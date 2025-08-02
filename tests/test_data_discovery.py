"""Test cases for data discovery module."""

import os
import tempfile
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, date
from src.data_discovery import DataDiscoveryEngine
from src.file_operations import ExcelFileManager


class TestDataDiscoveryEngine:
    """Test cases for DataDiscoveryEngine class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.discovery = DataDiscoveryEngine()
        self.file_manager = ExcelFileManager()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create comprehensive test data
        self.test_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', None, 'Eve'],
            'age': [25.5, 30, 35, 40, None],
            'salary': [50000, 60000, 75000, 80000, 55000],
            'is_active': [True, False, True, True, False],
            'join_date': pd.to_datetime(['2020-01-15', '2019-06-20', '2021-03-10', '2018-12-01', '2022-05-30']),
            'rating': [4.5, 3.8, 4.2, 4.9, 3.5]
        })
        
        self.test_file = os.path.join(self.temp_dir, 'test_data.xlsx')
        self.test_data.to_excel(self.test_file, index=False, sheet_name='Employees')
        
        # Create multi-sheet file
        self.multi_sheet_file = os.path.join(self.temp_dir, 'multi_sheet.xlsx')
        with pd.ExcelWriter(self.multi_sheet_file) as writer:
            self.test_data.to_excel(writer, sheet_name='Employees', index=False)
            pd.DataFrame({
                'category': ['A', 'B', 'A', 'C', 'B'],
                'value': [10, 20, 15, 25, 12]
            }).to_excel(writer, sheet_name='Categories', index=False)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        # Clean up temp files
        for file in [self.test_file, self.multi_sheet_file]:
            if os.path.exists(file):
                os.remove(file)
        os.rmdir(self.temp_dir)
        
        # Clear cache
        self.file_manager.clear_cache()
    
    def test_get_schema_success(self):
        """Test successful schema retrieval."""
        result = self.discovery.get_schema(self.test_file)
        
        assert result['success'] is True
        assert result['total_columns'] == 7
        assert result['total_rows'] == 5
        assert len(result['schema']) == 7
        
        # Check specific column schema
        name_col = next(col for col in result['schema'] if col['column_name'] == 'name')
        assert name_col['semantic_type'] == 'text'
        assert name_col['nullable'] is True
        assert name_col['null_count'] == 1
        
        age_col = next(col for col in result['schema'] if col['column_name'] == 'age')
        assert age_col['semantic_type'] == 'float'
        assert age_col['nullable'] is True
        
        is_active_col = next(col for col in result['schema'] if col['column_name'] == 'is_active')
        assert is_active_col['semantic_type'] == 'boolean'
        
        join_date_col = next(col for col in result['schema'] if col['column_name'] == 'join_date')
        assert join_date_col['semantic_type'] == 'datetime'
    
    def test_get_schema_specific_sheet(self):
        """Test schema retrieval for specific sheet."""
        result = self.discovery.get_schema(self.multi_sheet_file, 'Categories')
        
        assert result['success'] is True
        assert result['total_columns'] == 2
        assert result['sheet_name'] == 'Categories'
        
        category_col = next(col for col in result['schema'] if col['column_name'] == 'category')
        assert category_col['semantic_type'] == 'text'
        assert category_col['unique_count'] == 3
    
    def test_get_sample_data_head(self):
        """Test getting head sample data."""
        result = self.discovery.get_sample_data(self.test_file, rows=3, sample_type="head")
        
        assert result['success'] is True
        assert result['sample_type'] == 'head'
        assert result['requested_rows'] == 3
        assert result['returned_rows'] == 3
        assert len(result['data']) == 3
        assert result['data'][0]['id'] == 1
        assert result['data'][0]['name'] == 'Alice'
    
    def test_get_sample_data_tail(self):
        """Test getting tail sample data."""
        result = self.discovery.get_sample_data(self.test_file, rows=2, sample_type="tail")
        
        assert result['success'] is True
        assert result['sample_type'] == 'tail'
        assert result['returned_rows'] == 2
        assert result['data'][0]['id'] == 4
        assert result['data'][1]['id'] == 5
    
    def test_get_sample_data_random(self):
        """Test getting random sample data."""
        result = self.discovery.get_sample_data(self.test_file, rows=3, sample_type="random")
        
        assert result['success'] is True
        assert result['sample_type'] == 'random'
        assert result['returned_rows'] == 3
        # Should have 3 different IDs
        ids = [row['id'] for row in result['data']]
        assert len(set(ids)) == 3
    
    def test_get_sample_data_invalid_type(self):
        """Test invalid sample type."""
        result = self.discovery.get_sample_data(self.test_file, sample_type="invalid")
        
        assert 'error' in result
        assert 'Invalid sample_type' in result['error']
    
    def test_get_sample_data_invalid_rows(self):
        """Test invalid row count."""
        result = self.discovery.get_sample_data(self.test_file, rows=0)
        
        assert 'error' in result
        assert 'Number of rows must be positive' in result['error']
    
    def test_get_column_info_numeric(self):
        """Test detailed column info for numeric column."""
        result = self.discovery.get_column_info(self.test_file, 'salary')
        
        assert result['success'] is True
        assert result['column_name'] == 'salary'
        assert result['total_count'] == 5
        assert result['null_count'] == 0
        assert result['unique_count'] == 5
        assert result['min'] == 50000
        assert result['max'] == 80000
        assert 'mean' in result
        assert 'median' in result
        assert 'std' in result
        assert 'q25' in result
        assert 'q75' in result
        assert 'sample_values' in result
    
    def test_get_column_info_text(self):
        """Test detailed column info for text column."""
        result = self.discovery.get_column_info(self.test_file, 'name')
        
        assert result['success'] is True
        assert result['column_name'] == 'name'
        assert result['null_count'] == 1
        assert result['unique_count'] == 4  # One null
        assert 'top_values' in result
        assert 'sample_values' in result
        # Should not have numeric stats
        assert 'mean' not in result
        assert 'std' not in result
    
    def test_get_column_info_nonexistent(self):
        """Test column info for non-existent column."""
        result = self.discovery.get_column_info(self.test_file, 'nonexistent')
        
        assert 'error' in result
        assert 'Column \'nonexistent\' not found' in result['error']
    
    def test_get_dimensions(self):
        """Test getting dataset dimensions."""
        result = self.discovery.get_dimensions(self.test_file)
        
        assert result['success'] is True
        assert result['rows'] == 5
        assert result['columns'] == 7
        assert result['total_cells'] == 35
        assert result['memory_usage_mb'] >= 0  # Small datasets might have very small memory usage
        assert len(result['column_names']) == 7
        assert 'id' in result['column_names']
        assert 'dtypes' in result
        assert result['empty_rows'] == 0
        assert result['empty_columns'] == 0
    
    def test_describe_dataset_numeric_only(self):
        """Test dataset description with numeric columns only."""
        result = self.discovery.describe_dataset(self.test_file, include_all=False)
        
        assert result['success'] is True
        assert result['total_rows'] == 5
        assert result['total_columns'] == 7
        assert 'numeric_summary' in result
        assert 'categorical_summary' not in result
        
        # Check numeric columns are included
        assert 'age' in result['numeric_summary']
        assert 'salary' in result['numeric_summary']
        assert 'rating' in result['numeric_summary']
        
        # Check salary statistics
        salary_stats = result['numeric_summary']['salary']
        assert salary_stats['count'] == 5
        assert salary_stats['min'] == 50000
        assert salary_stats['max'] == 80000
        
        # Check data quality metrics
        assert 'data_quality' in result
        assert result['data_quality']['total_missing_values'] > 0  # We have nulls
        assert result['data_quality']['duplicate_rows'] == 0
        assert result['data_quality']['complete_rows'] == 3  # Only 3 rows without nulls
    
    def test_describe_dataset_include_all(self):
        """Test dataset description including categorical columns."""
        result = self.discovery.describe_dataset(self.test_file, include_all=True)
        
        assert result['success'] is True
        assert 'numeric_summary' in result
        assert 'categorical_summary' in result
        
        # Check categorical summary
        assert 'name' in result['categorical_summary']
        name_stats = result['categorical_summary']['name']
        assert name_stats['count'] == 4  # 4 non-null values
        assert name_stats['unique'] == 4
    
    def test_file_not_found_errors(self):
        """Test error handling for non-existent files."""
        nonexistent_file = '/nonexistent/file.xlsx'
        
        schema_result = self.discovery.get_schema(nonexistent_file)
        assert 'error' in schema_result
        
        sample_result = self.discovery.get_sample_data(nonexistent_file)
        assert 'error' in sample_result
        
        column_result = self.discovery.get_column_info(nonexistent_file, 'test')
        assert 'error' in column_result
        
        dim_result = self.discovery.get_dimensions(nonexistent_file)
        assert 'error' in dim_result
        
        desc_result = self.discovery.describe_dataset(nonexistent_file)
        assert 'error' in desc_result


class TestDataDiscoveryIntegration:
    """Integration tests using the actual sample data file."""
    
    def setup_method(self):
        """Set up integration test fixtures."""
        self.discovery = DataDiscoveryEngine()
        self.sample_file = 'data/food_reviews.xlsx'
    
    def teardown_method(self):
        """Clean up after integration tests."""
        self.discovery.file_manager.clear_cache()
    
    def test_sample_file_schema(self):
        """Test schema analysis of sample file."""
        if os.path.exists(self.sample_file):
            result = self.discovery.get_schema(self.sample_file)
            
            assert result['success'] is True
            assert result['total_columns'] > 0
            assert result['total_rows'] > 0
            
            print(f"Sample file schema: {result['total_rows']} rows, {result['total_columns']} columns")
            for col in result['schema'][:3]:  # Print first 3 columns
                print(f"  {col['column_name']}: {col['semantic_type']} (nulls: {col['null_count']})")
        else:
            pytest.skip("Sample file not found")
    
    def test_sample_file_sample_data(self):
        """Test sample data from sample file."""
        if os.path.exists(self.sample_file):
            result = self.discovery.get_sample_data(self.sample_file, rows=3)
            
            assert result['success'] is True
            assert len(result['data']) <= 3
            assert len(result['columns']) > 0
            
            print(f"Sample data columns: {result['columns']}")
            print(f"First row: {result['data'][0] if result['data'] else 'No data'}")
        else:
            pytest.skip("Sample file not found")
    
    def test_sample_file_description(self):
        """Test dataset description of sample file."""
        if os.path.exists(self.sample_file):
            result = self.discovery.describe_dataset(self.sample_file, include_all=True)
            
            assert result['success'] is True
            assert 'data_quality' in result
            
            print(f"Data quality: {result['data_quality']}")
            if 'numeric_summary' in result:
                print(f"Numeric columns: {list(result['numeric_summary'].keys())}")
            if 'categorical_summary' in result:
                print(f"Categorical columns: {list(result['categorical_summary'].keys())}")
        else:
            pytest.skip("Sample file not found")


if __name__ == '__main__':
    """Run tests directly."""
    pytest.main([__file__, '-v'])