# Test Plan: File Operations (Open, Save, Edit, Cancel)

This document provides a comprehensive test plan for testing file operations in the md2office GUI application, including opening files, saving files, editing content, and canceling modifications.

## Overview

The md2office GUI application provides a markdown editor with the following file operation capabilities:

- **Opening files**: Via menu, browse button, drag-and-drop
- **Saving files**: Save (to current file) and Save As (to new file)
- **Editing**: Real-time markdown editing with syntax highlighting
- **Canceling modifications**: Handling unsaved changes when opening new files, closing documents, or closing the window

## Test Scope

### Components Under Test

- `MainWindow` (`src/md2office/gui/main_window.py`)
- `MarkdownEditor` (`src/md2office/gui/widgets/markdown_editor.py`)

### Test Categories

1. **Unit Tests**: Individual component behavior
2. **Integration Tests**: Component interactions
3. **User Workflow Tests**: End-to-end user scenarios

## Test Cases

### 1. Opening Files

#### 1.1 Open File via Menu

**Test ID**: `TEST_OPEN_001`

**Description**: Test opening a file using File → Open menu

**Preconditions**:
- Application is running
- No file is currently open (or file can be closed)

**Test Steps**:
1. Click File → Open (or press Ctrl+O)
2. Select a valid markdown file from file dialog
3. Click Open

**Expected Results**:
- File content loads into editor
- File path displays in file path field
- Window title updates to show filename
- Modification indicator (*) is not shown
- Preview pane updates with file content
- `current_file` property is set correctly
- `is_modified` is `False`

**Test Data**:
- Valid markdown files: `examples/input/sample.md`, `examples/input/presentation-session-1-quick-wins.md`

---

#### 1.2 Open File via Browse Button

**Test ID**: `TEST_OPEN_002`

**Description**: Test opening a file using the Browse button

**Preconditions**:
- Application is running

**Test Steps**:
1. Click "Browse..." button next to Input File field
2. Select a valid markdown file
3. Click Open

**Expected Results**:
- Same as TEST_OPEN_001

---

#### 1.3 Open File via Drag and Drop

**Test ID**: `TEST_OPEN_003`

**Description**: Test opening a file by dragging and dropping it into the window

**Preconditions**:
- Application is running

**Test Steps**:
1. Drag a markdown file from file manager
2. Drop it onto the application window

**Expected Results**:
- Same as TEST_OPEN_001

---

#### 1.4 Open File - Cancel Dialog

**Test ID**: `TEST_OPEN_004`

**Description**: Test canceling the file open dialog

**Preconditions**:
- Application is running

**Test Steps**:
1. Click File → Open
2. Click Cancel in file dialog

**Expected Results**:
- File dialog closes
- No file is loaded
- Current state remains unchanged

---

#### 1.5 Open File - Invalid File Type

**Test ID**: `TEST_OPEN_005`

**Description**: Test attempting to open a non-markdown file via drag-and-drop

**Preconditions**:
- Application is running

**Test Steps**:
1. Drag a non-markdown file (e.g., `.txt`, `.docx`) onto window
2. Drop it

**Expected Results**:
- Warning message displayed: "Please drop a markdown (.md) file."
- File is not loaded
- Current state remains unchanged

---

#### 1.6 Open File - File Not Found

**Test ID**: `TEST_OPEN_006`

**Description**: Test opening a file that doesn't exist (programmatic)

**Preconditions**:
- Application is running

**Test Steps**:
1. Programmatically call `markdown_editor.load_file()` with non-existent path

**Expected Results**:
- `load_file()` returns `False`
- Error message displayed: "Could not open file: <path>"
- Current state remains unchanged

---

#### 1.7 Open File - Permission Denied

**Test ID**: `TEST_OPEN_007`

**Description**: Test opening a file without read permissions

**Preconditions**:
- Application is running
- A file exists but has no read permissions

**Test Steps**:
1. Attempt to open a file without read permissions

**Expected Results**:
- `load_file()` returns `False`
- Error message displayed
- Current state remains unchanged

---

### 2. Saving Files

#### 2.1 Save File - Existing File

**Test ID**: `TEST_SAVE_001`

**Description**: Test saving changes to an existing file

**Preconditions**:
- A file is open in the editor
- File has been modified

**Test Steps**:
1. Make changes to the file content
2. Click File → Save (or press Ctrl+S)
3. If overwrite dialog appears, choose "Overwrite"

**Expected Results**:
- File is saved successfully
- Success message displayed: "File saved successfully."
- `is_modified` becomes `False`
- Window title updates (removes * indicator)
- File on disk contains the new content

---

#### 2.2 Save File - New File (Save As)

**Test ID**: `TEST_SAVE_002`

**Description**: Test saving a new/untitled file using Save As

**Preconditions**:
- Editor contains content but no file is open (or untitled document)

**Test Steps**:
1. Enter content in editor
2. Click File → Save As (or press Ctrl+Shift+S)
3. Enter filename in save dialog
4. Click Save

**Expected Results**:
- File is saved successfully
- Success message displayed
- `current_file` is set to the new path
- File path field updates
- Window title updates with new filename
- `is_modified` becomes `False`
- File exists on disk with correct content

---

#### 2.3 Save File - Overwrite Existing File

**Test ID**: `TEST_SAVE_003`

**Description**: Test saving over an existing file (overwrite option)

**Preconditions**:
- A file is open
- File has been modified
- File exists on disk

**Test Steps**:
1. Make changes to file
2. Click File → Save
3. In overwrite dialog, select "Overwrite"

**Expected Results**:
- File is overwritten
- Success message displayed
- Original file content is replaced
- `is_modified` becomes `False`

---

#### 2.4 Save File - Create Backup

**Test ID**: `TEST_SAVE_004`

**Description**: Test saving with backup creation

**Preconditions**:
- A file is open
- File has been modified
- File exists on disk

**Test Steps**:
1. Make changes to file
2. Click File → Save
3. In overwrite dialog, select "Create Backup"

**Expected Results**:
- Backup file is created (with `.bak` extension or timestamp)
- Backup message displayed: "Backup created: <backup_name>"
- Original file is saved with new content
- Backup file contains original content
- `is_modified` becomes `False`

---

#### 2.5 Save File - Cancel Overwrite Dialog

**Test ID**: `TEST_SAVE_005`

**Description**: Test canceling the overwrite dialog

**Preconditions**:
- A file is open
- File has been modified
- File exists on disk

**Test Steps**:
1. Make changes to file
2. Click File → Save
3. In overwrite dialog, select "Cancel"

**Expected Results**:
- Save operation is cancelled
- File is not saved
- `is_modified` remains `True`
- Window title still shows * indicator
- Original file content unchanged

---

#### 2.6 Save File - Invalid Path

**Test ID**: `TEST_SAVE_006`

**Description**: Test saving to an invalid path (programmatic)

**Preconditions**:
- Application is running

**Test Steps**:
1. Programmatically call `save_file()` with invalid path (e.g., `/invalid/path/file.md`)

**Expected Results**:
- `save_file()` returns `False`
- Error message displayed: "Could not save file."
- File is not saved
- `is_modified` remains `True`

---

#### 2.7 Save File - Permission Denied

**Test ID**: `TEST_SAVE_007`

**Description**: Test saving to a file without write permissions

**Preconditions**:
- A file is open
- File exists but has no write permissions

**Test Steps**:
1. Make changes to file
2. Attempt to save

**Expected Results**:
- `save_file()` returns `False`
- Error message displayed
- File is not saved
- `is_modified` remains `True`

---

#### 2.8 Save File - No Current File (Save)

**Test ID**: `TEST_SAVE_008`

**Description**: Test Save when no file is open (should trigger Save As)

**Preconditions**:
- Editor has content but no file is open

**Test Steps**:
1. Enter content in editor
2. Click File → Save

**Expected Results**:
- Save As dialog opens automatically
- User can choose filename and save

---

### 3. Editing Files

#### 3.1 Edit Content - Basic Text

**Test ID**: `TEST_EDIT_001`

**Description**: Test basic text editing

**Preconditions**:
- A file is open

**Test Steps**:
1. Type text in the editor
2. Observe modification state

**Expected Results**:
- Text appears in editor
- `is_modified` becomes `True`
- Window title shows * indicator
- Preview updates after 500ms debounce
- Modification changed signal is emitted

---

#### 3.2 Edit Content - Syntax Highlighting

**Test ID**: `TEST_EDIT_002`

**Description**: Test that syntax highlighting works while editing

**Preconditions**:
- A file is open

**Test Steps**:
1. Type markdown syntax (headers, bold, italic, code, links)
2. Observe highlighting

**Expected Results**:
- Headers (#) are highlighted in blue and bold
- Bold text (**text**) is bold
- Italic text (*text*) is italic
- Inline code (`code`) has red text and pink background
- Links [text](url) are blue and underlined

---

#### 3.3 Edit Content - Preview Updates

**Test ID**: `TEST_EDIT_003`

**Description**: Test that preview updates when editing

**Preconditions**:
- A file is open

**Test Steps**:
1. Type markdown content
2. Wait for preview update (500ms debounce)

**Expected Results**:
- Preview pane updates with rendered markdown
- Preview reflects current editor content
- Images and relative paths resolve correctly (if applicable)

---

#### 3.4 Edit Content - Large File

**Test ID**: `TEST_EDIT_004`

**Description**: Test editing a large markdown file

**Preconditions**:
- A large markdown file is open (>1000 lines)

**Test Steps**:
1. Make edits throughout the file
2. Save the file

**Expected Results**:
- Editor remains responsive
- Syntax highlighting works correctly
- Preview updates correctly
- File saves successfully

---

#### 3.5 Edit Content - Undo/Redo

**Test ID**: `TEST_EDIT_005`

**Description**: Test undo/redo functionality (if implemented)

**Preconditions**:
- A file is open

**Test Steps**:
1. Type some text
2. Press Ctrl+Z (undo)
3. Press Ctrl+Y (redo)

**Expected Results**:
- Undo reverts changes
- Redo reapplies changes
- Modification state updates correctly

**Note**: Verify if undo/redo is implemented in QPlainTextEdit (should be by default)

---

### 4. Canceling Modifications

#### 4.1 Cancel - Open New File with Unsaved Changes (Save)

**Test ID**: `TEST_CANCEL_001`

**Description**: Test opening a new file when current file has unsaved changes - user chooses Save

**Preconditions**:
- A file is open
- File has been modified (unsaved changes)

**Test Steps**:
1. Make changes to current file
2. Click File → Open
3. In unsaved changes dialog, select "Save"
4. Complete save operation (handle overwrite if needed)
5. File dialog opens

**Expected Results**:
- Unsaved changes dialog appears: "You have unsaved changes. Do you want to save them before continuing?"
- After saving, file dialog opens
- User can select new file
- New file loads successfully

---

#### 4.2 Cancel - Open New File with Unsaved Changes (Discard)

**Test ID**: `TEST_CANCEL_002`

**Description**: Test opening a new file when current file has unsaved changes - user chooses Discard

**Preconditions**:
- A file is open
- File has been modified

**Test Steps**:
1. Make changes to current file
2. Click File → Open
3. In unsaved changes dialog, select "Discard"
4. Select new file in file dialog

**Expected Results**:
- Unsaved changes dialog appears
- After discarding, file dialog opens
- Changes are discarded (file reloads from disk if it exists)
- New file loads successfully
- `is_modified` becomes `False`

---

#### 4.3 Cancel - Open New File with Unsaved Changes (Cancel)

**Test ID**: `TEST_CANCEL_003`

**Description**: Test opening a new file when current file has unsaved changes - user chooses Cancel

**Preconditions**:
- A file is open
- File has been modified

**Test Steps**:
1. Make changes to current file
2. Click File → Open
3. In unsaved changes dialog, select "Cancel"

**Expected Results**:
- Unsaved changes dialog appears
- File dialog does not open
- Current file remains open
- Changes are preserved
- `is_modified` remains `True`

---

#### 4.4 Cancel - Close Document with Unsaved Changes (Save)

**Test ID**: `TEST_CANCEL_004`

**Description**: Test closing document when file has unsaved changes - user chooses Save

**Preconditions**:
- A file is open
- File has been modified

**Test Steps**:
1. Make changes to file
2. Click File → Close
3. In unsaved changes dialog, select "Save"
4. Complete save operation

**Expected Results**:
- Unsaved changes dialog appears
- File is saved
- Document closes (editor clears)
- File path field clears
- Window title updates to "Untitled"

---

#### 4.5 Cancel - Close Document with Unsaved Changes (Discard)

**Test ID**: `TEST_CANCEL_005`

**Description**: Test closing document when file has unsaved changes - user chooses Discard

**Preconditions**:
- A file is open
- File has been modified

**Test Steps**:
1. Make changes to file
2. Click File → Close
3. In unsaved changes dialog, select "Discard"

**Expected Results**:
- Unsaved changes dialog appears
- Changes are discarded
- Document closes
- File path field clears
- Window title updates

---

#### 4.6 Cancel - Close Document with Unsaved Changes (Cancel)

**Test ID**: `TEST_CANCEL_006`

**Description**: Test closing document when file has unsaved changes - user chooses Cancel

**Preconditions**:
- A file is open
- File has been modified

**Test Steps**:
1. Make changes to file
2. Click File → Close
3. In unsaved changes dialog, select "Cancel"

**Expected Results**:
- Unsaved changes dialog appears
- Document does not close
- Current file remains open
- Changes are preserved

---

#### 4.7 Cancel - Close Window with Unsaved Changes (Save)

**Test ID**: `TEST_CANCEL_007`

**Description**: Test closing window when file has unsaved changes - user chooses Save

**Preconditions**:
- A file is open
- File has been modified

**Test Steps**:
1. Make changes to file
2. Click window close button (or File → Exit)
3. In unsaved changes dialog, select "Save"
4. Complete save operation

**Expected Results**:
- Unsaved changes dialog appears
- File is saved
- Window closes
- Application exits

---

#### 4.8 Cancel - Close Window with Unsaved Changes (Discard)

**Test ID**: `TEST_CANCEL_008`

**Description**: Test closing window when file has unsaved changes - user chooses Discard

**Preconditions**:
- A file is open
- File has been modified

**Test Steps**:
1. Make changes to file
2. Click window close button
3. In unsaved changes dialog, select "Discard"

**Expected Results**:
- Unsaved changes dialog appears
- Changes are discarded
- Window closes
- Application exits

---

#### 4.9 Cancel - Close Window with Unsaved Changes (Cancel)

**Test ID**: `TEST_CANCEL_009`

**Description**: Test closing window when file has unsaved changes - user chooses Cancel

**Preconditions**:
- A file is open
- File has been modified

**Test Steps**:
1. Make changes to file
2. Click window close button
3. In unsaved changes dialog, select "Cancel"

**Expected Results**:
- Unsaved changes dialog appears
- Window does not close
- Application continues running
- Changes are preserved

---

#### 4.10 Cancel - Drag and Drop with Unsaved Changes (Save)

**Test ID**: `TEST_CANCEL_010`

**Description**: Test drag-and-drop when file has unsaved changes - user chooses Save

**Preconditions**:
- A file is open
- File has been modified

**Test Steps**:
1. Make changes to file
2. Drag a new markdown file onto window
3. In unsaved changes dialog, select "Save"
4. Complete save operation

**Expected Results**:
- Unsaved changes dialog appears
- File is saved
- New file loads after save completes

---

#### 4.11 Cancel - Drag and Drop with Unsaved Changes (Discard)

**Test ID**: `TEST_CANCEL_011`

**Description**: Test drag-and-drop when file has unsaved changes - user chooses Discard

**Preconditions**:
- A file is open
- File has been modified

**Test Steps**:
1. Make changes to file
2. Drag a new markdown file onto window
3. In unsaved changes dialog, select "Discard"

**Expected Results**:
- Unsaved changes dialog appears
- Changes are discarded
- New file loads

---

#### 4.12 Cancel - Drag and Drop with Unsaved Changes (Cancel)

**Test ID**: `TEST_CANCEL_012`

**Description**: Test drag-and-drop when file has unsaved changes - user chooses Cancel

**Preconditions**:
- A file is open
- File has been modified

**Test Steps**:
1. Make changes to file
2. Drag a new markdown file onto window
3. In unsaved changes dialog, select "Cancel"

**Expected Results**:
- Unsaved changes dialog appears
- Drop operation is cancelled (event.ignore())
- Current file remains open
- Changes are preserved
- New file is not loaded

---

#### 4.13 Cancel - New File with Unsaved Changes

**Test ID**: `TEST_CANCEL_013`

**Description**: Test creating new file when current file has unsaved changes

**Preconditions**:
- A file is open
- File has been modified

**Test Steps**:
1. Make changes to file
2. Click File → New
3. Handle unsaved changes dialog (test all three options)

**Expected Results**:
- Unsaved changes dialog appears
- After Save/Discard, new file is created
- After Cancel, new file is not created

---

#### 4.14 Cancel - No Unsaved Changes

**Test ID**: `TEST_CANCEL_014`

**Description**: Test that no dialog appears when there are no unsaved changes

**Preconditions**:
- A file is open
- File has no unsaved changes (saved or not modified)

**Test Steps**:
1. Open a file (or save current file)
2. Click File → Open (or File → Close, or window close)

**Expected Results**:
- No unsaved changes dialog appears
- Operation proceeds immediately
- File opens/closes/window closes without prompt

---

### 5. Integration Tests

#### 5.1 Complete Workflow - Open, Edit, Save

**Test ID**: `TEST_INTEGRATION_001`

**Description**: Test complete workflow of opening, editing, and saving a file

**Preconditions**:
- Application is running

**Test Steps**:
1. Open a file
2. Make multiple edits
3. Save the file
4. Close the file
5. Reopen the file

**Expected Results**:
- File opens correctly
- Edits are tracked
- File saves with all changes
- Reopened file contains saved changes

---

#### 5.2 Complete Workflow - New File, Edit, Save As

**Test ID**: `TEST_INTEGRATION_002`

**Description**: Test creating new file, editing, and saving with Save As

**Preconditions**:
- Application is running

**Test Steps**:
1. Start with new/empty document
2. Enter markdown content
3. Save As with new filename
4. Make additional edits
5. Save (should save to same file)

**Expected Results**:
- New file created successfully
- Content saved correctly
- Subsequent saves update the same file
- Window title updates correctly

---

#### 5.3 Complete Workflow - Multiple Files

**Test ID**: `TEST_INTEGRATION_003`

**Description**: Test opening and switching between multiple files

**Preconditions**:
- Application is running
- Multiple markdown files exist

**Test Steps**:
1. Open file A
2. Make changes
3. Save file A
4. Open file B (should prompt for unsaved changes if any)
5. Make changes to file B
6. Save file B
7. Open file A again

**Expected Results**:
- Files switch correctly
- Each file maintains its own state
- Unsaved changes are handled correctly
- File content is preserved

---

## Test Implementation Notes

### Test Fixtures

Create reusable fixtures for common scenarios:

```python
@pytest.fixture
def sample_markdown_file(tmp_path):
    """Create a sample markdown file for testing."""
    file_path = tmp_path / "test.md"
    file_path.write_text("# Test Document\n\nThis is a test.")
    return file_path

@pytest.fixture
def modified_file(tmp_path):
    """Create a file with unsaved modifications."""
    file_path = tmp_path / "test.md"
    file_path.write_text("# Original")
    return file_path
```

### Mocking File Dialogs

Use mocking to avoid actual file dialogs in tests:

```python
from unittest.mock import patch, MagicMock

@patch('PySide6.QtWidgets.QFileDialog.getOpenFileName')
def test_open_file(mock_dialog, main_window, sample_markdown_file):
    mock_dialog.return_value = (str(sample_markdown_file), None)
    # Test implementation
```

### Testing Signals

Test signal emissions:

```python
from PySide6.QtTest import QSignalSpy

def test_modification_signal(main_window):
    spy = QSignalSpy(main_window.markdown_editor.modification_changed)
    main_window.markdown_editor.setPlainText("New content")
    assert len(spy) == 1
    assert spy[0][0] == True
```

### Testing Window Title Updates

Verify window title changes:

```python
def test_window_title_updates(main_window, sample_markdown_file):
    main_window.markdown_editor.load_file(sample_markdown_file)
    assert "test.md" in main_window.windowTitle()
    assert "*" not in main_window.windowTitle()
    
    main_window.markdown_editor.setPlainText("Modified")
    assert "*" in main_window.windowTitle()
```

## Test Execution

### Running Specific Test Categories

```bash
# Run all file operation tests
pytest tests/gui/test_file_operations.py -v

# Run only open tests
pytest tests/gui/test_file_operations.py::TestFileOpen -v

# Run only save tests
pytest tests/gui/test_file_operations.py::TestFileSave -v

# Run only cancel tests
pytest tests/gui/test_file_operations.py::TestCancelOperations -v
```

### Test Coverage Goals

- **Target Coverage**: 90%+ for file operation code paths
- **Critical Paths**: 100% coverage for unsaved changes handling
- **Edge Cases**: All error conditions should be tested

## Test Data Requirements

### Sample Files Needed

1. **Valid markdown files**:
   - Simple markdown (`simple.md`)
   - Complex markdown with all features (`complex.md`)
   - Large file (>1000 lines) (`large.md`)

2. **Invalid files**:
   - Non-markdown files (`.txt`, `.docx`)
   - Non-existent files
   - Files without read permissions
   - Files without write permissions

3. **Test scenarios**:
   - Empty files
   - Files with special characters
   - Files with unicode content
   - Files with very long lines

## Success Criteria

All tests should pass with:

- ✅ No test failures
- ✅ No test errors
- ✅ 90%+ code coverage for file operations
- ✅ All critical paths covered
- ✅ All edge cases handled
- ✅ Proper error messages displayed
- ✅ User experience is smooth and intuitive

## Known Issues and Limitations

- File dialogs require mocking for automated testing
- Some file permission tests may require platform-specific setup
- Drag-and-drop testing may require additional setup

## Future Enhancements

- Add tests for keyboard shortcuts (Ctrl+O, Ctrl+S, etc.)
- Add tests for file watching (if implemented)
- Add tests for recent files list (if implemented)
- Add performance tests for large files
- Add accessibility tests for file operations

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Author**: Test Plan Generator  
**Status**: Draft - Ready for Implementation

