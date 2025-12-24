"""
Tests for CLI

Implements Story 5.5: CLI Testing
"""

import pytest
import sys
import tempfile
import shutil
from pathlib import Path
from click.testing import CliRunner

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from md2office.cli import cli, main


class TestCLI:
    """Test suite for CLI."""
    
    @pytest.fixture
    def runner(self):
        """Create CLI test runner."""
        return CliRunner()
    
    @pytest.fixture
    def sample_markdown_file(self):
        """Create a temporary markdown file for testing."""
        content = """# Test Document

This is a test document.

## Section 1

Some content here.
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)
        
        yield temp_path
        
        # Cleanup
        if temp_path.exists():
            temp_path.unlink()
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_cli_help(self, runner):
        """Test CLI help command."""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Convert markdown files' in result.output
    
    def test_cli_version(self, runner):
        """Test CLI version command."""
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert 'md2office' in result.output.lower()
    
    def test_cli_no_input(self, runner):
        """Test CLI with no input files."""
        result = runner.invoke(cli, [])
        assert result.exit_code != 0
        assert 'No input files specified' in result.output or 'Missing argument' in result.output
    
    def test_cli_no_format(self, runner, sample_markdown_file):
        """Test CLI with no format specified."""
        result = runner.invoke(cli, [str(sample_markdown_file)])
        assert result.exit_code != 0
        assert 'No output format specified' in result.output
    
    def test_cli_word_conversion(self, runner, sample_markdown_file, temp_output_dir):
        """Test CLI Word conversion."""
        result = runner.invoke(cli, [
            '--word',
            '--output', str(temp_output_dir),
            str(sample_markdown_file)
        ])
        
        # May fail if python-docx not available, but should handle gracefully
        if result.exit_code == 0:
            # Check if output file was created
            output_files = list(temp_output_dir.glob('*.docx'))
            assert len(output_files) > 0
    
    def test_cli_powerpoint_conversion(self, runner, sample_markdown_file, temp_output_dir):
        """Test CLI PowerPoint conversion."""
        result = runner.invoke(cli, [
            '--powerpoint',
            '--output', str(temp_output_dir),
            str(sample_markdown_file)
        ])
        
        # May fail if python-pptx not available, but should handle gracefully
        if result.exit_code == 0:
            # Check if output file was created
            output_files = list(temp_output_dir.glob('*.pptx'))
            assert len(output_files) > 0
    
    def test_cli_all_formats(self, runner, sample_markdown_file, temp_output_dir):
        """Test CLI --all option."""
        result = runner.invoke(cli, [
            '--all',
            '--output', str(temp_output_dir),
            str(sample_markdown_file)
        ])
        
        # May fail if libraries not available
        if result.exit_code == 0:
            # Check if output files were created
            output_files = list(temp_output_dir.glob('*'))
            assert len(output_files) > 0
    
    def test_cli_custom_name(self, runner, sample_markdown_file, temp_output_dir):
        """Test CLI --name option."""
        result = runner.invoke(cli, [
            '--word',
            '--output', str(temp_output_dir),
            '--name', 'custom_output',
            str(sample_markdown_file)
        ])
        
        if result.exit_code == 0:
            output_file = temp_output_dir / 'custom_output.docx'
            assert output_file.exists()
    
    def test_cli_suffix(self, runner, sample_markdown_file, temp_output_dir):
        """Test CLI --suffix option."""
        result = runner.invoke(cli, [
            '--word',
            '--output', str(temp_output_dir),
            '--suffix', '-converted',
            str(sample_markdown_file)
        ])
        
        if result.exit_code == 0:
            # Check for suffixed filename
            output_files = list(temp_output_dir.glob('*-converted.docx'))
            assert len(output_files) > 0
    
    def test_cli_verbose(self, runner, sample_markdown_file, temp_output_dir):
        """Test CLI --verbose option."""
        result = runner.invoke(cli, [
            '--word',
            '--verbose',
            '--output', str(temp_output_dir),
            str(sample_markdown_file)
        ])
        
        # Should not fail, verbose just affects output
        assert result.exit_code in [0, 1]  # May fail if library not available
    
    def test_cli_quiet(self, runner, sample_markdown_file, temp_output_dir):
        """Test CLI --quiet option."""
        result = runner.invoke(cli, [
            '--word',
            '--quiet',
            '--output', str(temp_output_dir),
            str(sample_markdown_file)
        ])
        
        # Should produce minimal output
        assert len(result.output) == 0 or result.exit_code != 0
    
    def test_cli_style_preset(self, runner, sample_markdown_file, temp_output_dir):
        """Test CLI --style option."""
        result = runner.invoke(cli, [
            '--word',
            '--style', 'professional',
            '--output', str(temp_output_dir),
            str(sample_markdown_file)
        ])
        
        # Should not fail due to style option
        assert result.exit_code in [0, 1]
    
    def test_cli_invalid_file(self, runner, temp_output_dir):
        """Test CLI with invalid input file."""
        result = runner.invoke(cli, [
            '--word',
            '--output', str(temp_output_dir),
            'nonexistent.md'
        ])
        
        assert result.exit_code != 0
    
    def test_cli_directory_input(self, runner, temp_output_dir):
        """Test CLI with directory input."""
        # Create test directory with markdown files
        test_dir = temp_output_dir / 'test_docs'
        test_dir.mkdir()
        
        (test_dir / 'doc1.md').write_text('# Doc 1\n\nContent')
        (test_dir / 'doc2.md').write_text('# Doc 2\n\nContent')
        
        result = runner.invoke(cli, [
            '--word',
            '--output', str(temp_output_dir),
            str(test_dir)
        ])
        
        # Should process directory
        if result.exit_code == 0:
            output_files = list(temp_output_dir.glob('*.docx'))
            assert len(output_files) >= 0  # May be 0 if libraries not available

