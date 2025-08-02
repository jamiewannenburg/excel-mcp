"""Test cases for file operations module."""

import os
import tempfile
import pytest
import pandas as pd
from pathlib import Path
from src.file_operations import ExcelFileManager


class TestExcelFileManager:
    """Test cases for ExcelFileManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = ExcelFileManager()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test Excel file
        self.test_data = pd.DataFrame({
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'London', 'Tokyo']
        })
        
        self.test_file = os.path.join(self.temp_dir, 'test.xlsx')
        self.test_data.to_excel(self.test_file, index=False, sheet_name='Sheet1')
        
        # Create multi-sheet Excel file
        self.multi_sheet_file = os.path.join(self.temp_dir, 'multi_sheet.xlsx')
        with pd.ExcelWriter(self.multi_sheet_file) as writer:
            self.test_data.to_excel(writer, sheet_name='Data', index=False)
            pd.DataFrame({'X': [1, 2], 'Y': [3, 4]}).to_excel(writer, sheet_name='Numbers', index=False)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        # Clean up temp files
        for file in [self.test_file, self.multi_sheet_file]:
            if os.path.exists(file):
                os.remove(file)
        os.rmdir(self.temp_dir)
        
        # Clear cache
        self.manager.clear_cache()
    
    def test_load_excel_success(self):
        """Test successful Excel file loading."""
        result = self.manager.load_excel(self.test_file)
        
        assert result['success'] is True
        assert result['file_path'] == self.test_file
        assert result['sheet_name'] == 'Sheet1'
        assert result['rows'] == 3
        assert result['columns'] == 3
        assert result['column_names'] == ['Name', 'Age', 'City']
        assert 'cache_key' in result
    
    def test_load_excel_specific_sheet(self):
        """Test loading specific sheet from multi-sheet file."""
        result = self.manager.load_excel(self.multi_sheet_file, 'Numbers')
        
        assert result['success'] is True
        assert result['sheet_name'] == 'Numbers'
        assert result['rows'] == 2
        assert result['columns'] == 2
        assert result['column_names'] == ['X', 'Y']
    
    def test_load_excel_file_not_found(self):
        """Test loading non-existent file."""
        result = self.manager.load_excel('/nonexistent/file.xlsx')
        
        assert 'error' in result
        assert 'File not found' in result['error']
    
    def test_load_excel_invalid_extension(self):
        """Test loading file with invalid extension."""
        txt_file = os.path.join(self.temp_dir, 'test.txt')
        with open(txt_file, 'w') as f:
            f.write('test')
        
        result = self.manager.load_excel(txt_file)
        
        assert 'error' in result
        assert 'Invalid file type' in result['error']
        
        os.remove(txt_file)
    
    def test_list_sheets_success(self):
        """Test successful sheet listing."""
        result = self.manager.list_sheets(self.multi_sheet_file)
        
        assert result['success'] is True
        assert result['file_path'] == self.multi_sheet_file
        assert result['sheet_count'] == 2
        assert set(result['sheet_names']) == {'Data', 'Numbers'}
    
    def test_list_sheets_single_sheet(self):
        """Test listing sheets for single-sheet file."""
        result = self.manager.list_sheets(self.test_file)
        
        assert result['success'] is True
        assert result['sheet_count'] == 1
        assert result['sheet_names'] == ['Sheet1']
    
    def test_list_sheets_file_not_found(self):
        """Test listing sheets for non-existent file."""
        result = self.manager.list_sheets('/nonexistent/file.xlsx')
        
        assert 'error' in result
        assert 'File not found' in result['error']
    
    def test_get_file_info_success(self):
        """Test successful file info retrieval."""
        result = self.manager.get_file_info(self.test_file)
        
        assert result['success'] is True
        assert result['file_path'] == self.test_file
        assert result['file_name'] == 'test.xlsx'
        assert result['file_size'] > 0
        assert result['file_size_mb'] >= 0  # Small test files might have very small size
        assert result['file_type'] == 'Excel'
        assert result['sheet_count'] == 1
        assert result['sheet_names'] == ['Sheet1']
        assert 'created_date' in result
        assert 'modified_date' in result
    
    def test_get_file_info_non_excel(self):
        """Test file info for non-Excel file."""
        txt_file = os.path.join(self.temp_dir, 'test.txt')
        with open(txt_file, 'w') as f:
            f.write('test content')
        
        result = self.manager.get_file_info(txt_file)
        
        assert result['success'] is True
        assert result['file_type'] == '.txt'
        assert 'sheet_count' not in result
        
        os.remove(txt_file)
    
    def test_get_file_info_file_not_found(self):
        """Test file info for non-existent file."""
        result = self.manager.get_file_info('/nonexistent/file.xlsx')
        
        assert 'error' in result
        assert 'File not found' in result['error']
    
    def test_caching_functionality(self):
        """Test that data is properly cached."""
        # Load file
        result = self.manager.load_excel(self.test_file)
        cache_key = result['cache_key']
        
        # Check cache
        cached_data = self.manager.get_cached_data(cache_key)
        assert cached_data is not None
        assert len(cached_data) == 3
        assert list(cached_data.columns) == ['Name', 'Age', 'City']
    
    def test_clear_cache(self):
        """Test cache clearing."""
        # Load file to populate cache
        self.manager.load_excel(self.test_file)
        
        # Clear cache
        result = self.manager.clear_cache()
        
        assert result['success'] is True
        assert result['cleared_files'] == 1
        
        # Verify cache is empty
        assert len(self.manager._cached_files) == 0


class TestFileOperationsIntegration:
    """Integration tests using the actual sample data file."""
    
    def setup_method(self):
        """Set up integration test fixtures."""
        self.manager = ExcelFileManager()
        self.sample_file = 'data/food_reviews.xlsx'
    
    def teardown_method(self):
        """Clean up after integration tests."""
        self.manager.clear_cache()
    
    def test_load_sample_file(self):
        """Test loading the actual sample file if it exists."""
        if os.path.exists(self.sample_file):
            result = self.manager.load_excel(self.sample_file)
            
            # Should successfully load
            assert result['success'] is True
            assert result['rows'] > 0
            assert result['columns'] > 0
            assert len(result['column_names']) > 0
            
            print(f"Sample file loaded: {result['rows']} rows, {result['columns']} columns")
            print(f"Columns: {result['column_names']}")
        else:
            pytest.skip("Sample file not found")
    
    def test_list_sample_file_sheets(self):
        """Test listing sheets in sample file."""
        if os.path.exists(self.sample_file):
            result = self.manager.list_sheets(self.sample_file)
            
            assert result['success'] is True
            assert result['sheet_count'] > 0
            
            print(f"Sample file sheets: {result['sheet_names']}")
        else:
            pytest.skip("Sample file not found")


if __name__ == '__main__':
    """Run tests directly."""
    pytest.main([__file__, '-v'])