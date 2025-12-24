# Media Handling Specification

## Overview

This specification defines how images and media files are processed, optimized, embedded, and positioned in Word, PowerPoint, and PDF output formats. The specification ensures proper handling of all media types, optimization for file size and quality, and consistent presentation across all output formats.

### Media Handling Goals

1. **Proper Embedding**: Embed images correctly in all output formats
2. **Optimization**: Optimize images for file size while maintaining quality
3. **Consistent Presentation**: Ensure consistent image appearance across formats
4. **Error Handling**: Handle missing or broken media gracefully
5. **Accessibility**: Preserve alt text and accessibility information

### Media Handling Approach

The media handling process follows these steps:
1. **Discovery**: Identify all image and media references in markdown
2. **Path Resolution**: Resolve relative and absolute paths
3. **Loading**: Load image files from filesystem or URLs
4. **Processing**: Optimize, resize, and convert images as needed
5. **Embedding**: Embed images in output documents
6. **Error Handling**: Handle missing or broken references gracefully

## Image Processing

### Supported Image Formats

#### Input Formats

| Format | Extension | Support Level | Notes |
|--------|-----------|---------------|-------|
| PNG | .png | Full | Supports transparency, lossless |
| JPEG | .jpg, .jpeg | Full | Lossy compression, no transparency |
| GIF | .gif | Full | Supports animation, limited colors |
| SVG | .svg | Partial | Converted to PNG for embedding |
| WebP | .webp | Partial | Converted to PNG/JPEG for embedding |
| BMP | .bmp | Partial | Converted to PNG/JPEG |
| TIFF | .tiff, .tif | Partial | Converted to PNG/JPEG |

#### Output Formats

| Format | Word | PowerPoint | PDF | Notes |
|--------|------|------------|-----|-------|
| PNG | Yes | Yes | Yes | Preferred for graphics with transparency |
| JPEG | Yes | Yes | Yes | Preferred for photographs |
| GIF | Yes | Yes | Partial | May lose animation in some formats |

### Image Optimization

#### Compression Strategy

**JPEG Compression**:
- **Quality Setting**: 85% (good balance of quality and file size)
- **Progressive Encoding**: Optional (for web compatibility)
- **Color Space**: sRGB (standard color space)
- **Target File Size**: < 500KB per image (configurable)

**PNG Compression**:
- **Compression Level**: 6 (balanced compression)
- **Color Depth**: Preserve original (8-bit or 24-bit)
- **Transparency**: Preserve alpha channel
- **Target File Size**: < 1MB per image (configurable)

**GIF Optimization**:
- **Color Palette**: Optimize palette (256 colors max)
- **Dithering**: Apply dithering if needed
- **Animation**: Preserve animation (if supported by format)

#### Format Conversion

**SVG to PNG**:
- **Rasterization**: Convert SVG to PNG at appropriate resolution
- **Resolution**: 300 DPI for high quality, 150 DPI for standard
- **Background**: White background (or transparent if SVG has transparency)
- **Size**: Match SVG viewBox dimensions or scale appropriately

**WebP to PNG/JPEG**:
- **Conversion**: Convert WebP to PNG (for graphics) or JPEG (for photos)
- **Quality**: Maintain quality during conversion
- **Transparency**: Preserve transparency (PNG) or add white background (JPEG)

### Image Sizing

#### Size Constraints

| Format | Maximum Width | Maximum Height | Aspect Ratio | Notes |
|--------|---------------|----------------|--------------|-------|
| Word | 6.5" (780px @ 120 DPI) | 9" (1080px @ 120 DPI) | Preserved | Page width minus margins |
| PowerPoint | 9.5" (1140px @ 120 DPI) | 7" (840px @ 120 DPI) | Preserved | Slide width minus margins |
| PDF | 6" (720px @ 120 DPI) | 9" (1080px @ 120 DPI) | Preserved | Content width |

#### Scaling Rules

1. **Scale Down**: Scale down images that exceed maximum dimensions
2. **Preserve Aspect Ratio**: Always maintain aspect ratio
3. **Scale Up**: Optionally scale up small images (configurable, default: no)
4. **Resolution**: Maintain appropriate resolution (120-300 DPI)

#### Sizing Strategy

- **Large Images**: Scale down to fit within format constraints
- **Small Images**: Preserve original size (unless very small)
- **Aspect Ratio**: Always preserve aspect ratio
- **Quality**: Maintain image quality during scaling

### Image Quality Settings

#### Resolution Requirements

| Format | Minimum DPI | Optimal DPI | Maximum DPI | Notes |
|--------|------------|------------|-------------|-------|
| Word | 96 | 150 | 300 | Screen viewing |
| PowerPoint | 96 | 150 | 300 | Screen viewing |
| PDF | 150 | 200 | 300 | Print quality |

#### Quality Targets

- **Screen Viewing**: 96-150 DPI sufficient
- **Print Quality**: 200-300 DPI recommended
- **File Size**: Balance quality and file size
- **Compression**: Apply compression while maintaining visual quality

## Format-Specific Image Handling

### Word Image Handling

#### Embedding Method

- **Embedding Type**: Inline embedding (images embedded in document)
- **Storage**: Images stored as binary data in .docx file
- **Format**: PNG or JPEG (based on image type)
- **Compression**: Apply compression during embedding

#### Image Properties

- **Positioning**: Inline with text flow
- **Text Wrapping**: Inline (no text wrapping around image)
- **Alignment**: Left-aligned (default), center/right if specified
- **Sizing**: Preserve aspect ratio, scale to fit width

#### Image Format Selection

- **Graphics/Logos**: PNG (preserves transparency)
- **Photographs**: JPEG (better compression)
- **Screenshots**: PNG (preserves text clarity)

#### Alt Text Handling

- **Storage**: Store alt text in image properties
- **Accessibility**: Enable screen reader support
- **Preservation**: Preserve alt text from markdown

### PowerPoint Image Handling

#### Embedding Method

- **Embedding Type**: Slide image embedding
- **Storage**: Images stored as binary data in .pptx file
- **Format**: PNG (preferred for transparency and quality)
- **Compression**: Apply compression during embedding

#### Image Properties

- **Positioning**: On slide in content area
- **Placement**: Centered or as specified by slide layout
- **Sizing**: Fit to slide width (max 9.5"), preserve aspect ratio
- **Layout**: Respect slide layout constraints

#### Image Format Selection

- **All Images**: PNG preferred (better quality, transparency support)
- **Large Images**: May use JPEG for file size (if transparency not needed)
- **Logos/Graphics**: PNG (preserves transparency)

#### Alt Text Handling

- **Storage**: Store alt text in image properties
- **Accessibility**: Enable screen reader support
- **Preservation**: Preserve alt text from markdown

### PDF Image Handling

#### Embedding Method

- **Embedding Type**: PDF image object embedding
- **Storage**: Images embedded as PDF image objects
- **Format**: JPEG (for photos) or PNG (for graphics)
- **Compression**: Use PDF image compression

#### Image Properties

- **Positioning**: Inline with text flow or block placement
- **Alignment**: Left-aligned (default), center/right if specified
- **Sizing**: Preserve aspect ratio, scale to fit width
- **Resolution**: Maintain appropriate resolution (150-300 DPI)

#### Image Format Selection

- **Photographs**: JPEG (better compression for photos)
- **Graphics/Logos**: PNG (preserves transparency and quality)
- **Screenshots**: PNG (preserves text clarity)

#### Alt Text Handling

- **Storage**: Store alt text in image metadata
- **Accessibility**: Enable screen reader support
- **Preservation**: Preserve alt text from markdown

## Placement Strategies

### Inline Images

#### Definition

Images referenced inline with text in markdown are placed inline at their reference location.

#### Placement Rules

1. **Position**: Place image at exact markdown reference location
2. **Flow**: Image flows with text (inline positioning)
3. **Spacing**: 6pt spacing before and after image
4. **Alignment**: Left-aligned (default), center/right if specified

#### Format-Specific Behavior

- **Word**: Inline image, flows with text
- **PowerPoint**: Image on slide at content position
- **PDF**: Inline image, flows with text

### Standalone Images

#### Definition

Images in their own paragraph (blank line before and after) are treated as standalone images.

#### Placement Rules

1. **Position**: Centered on page/slide (default)
2. **Spacing**: 6pt spacing before and after
3. **Sizing**: Scale to fit content width
4. **Alignment**: Center-aligned (default)

#### Format-Specific Behavior

- **Word**: Centered paragraph with image
- **PowerPoint**: Centered image on slide
- **PDF**: Centered image block

### Image with Caption

#### Definition

Images followed by caption text (in parentheses or separate paragraph) are treated as figures.

#### Placement Rules

1. **Image**: Place image with appropriate sizing
2. **Caption**: Place caption below image
3. **Formatting**: Caption in smaller font (9pt), italic
4. **Alignment**: Center-aligned (image and caption)

#### Format-Specific Behavior

- **Word**: Image with caption below
- **PowerPoint**: Image with caption on slide
- **PDF**: Image with caption block

### Image Positioning Options

#### Left Alignment

- **Usage**: Images aligned to left margin
- **Text Wrapping**: Text flows to right of image (if supported)
- **Application**: Word (with text wrapping), PDF (block placement)

#### Center Alignment

- **Usage**: Images centered on page/slide
- **Application**: All formats (default for standalone images)

#### Right Alignment

- **Usage**: Images aligned to right margin
- **Text Wrapping**: Text flows to left of image (if supported)
- **Application**: Word (with text wrapping), PDF (block placement)

## Media File Handling

### Video Files

#### Support Level

- **Word**: Limited (link to video file, no embedding)
- **PowerPoint**: Full (embed video files)
- **PDF**: Limited (link to video file, no embedding)

#### Handling Strategy

1. **Detection**: Identify video file references in markdown
2. **Format Support**: Check format support for target output
3. **Embedding**: Embed in PowerPoint, link in Word/PDF
4. **Fallback**: Use placeholder image with link if embedding not possible

#### Video Format Support

- **PowerPoint**: MP4, WMV, AVI (format-dependent)
- **Word/PDF**: Link to video file (no embedding)

### Audio Files

#### Support Level

- **Word**: Limited (link to audio file, no embedding)
- **PowerPoint**: Full (embed audio files)
- **PDF**: Limited (link to audio file, no embedding)

#### Handling Strategy

1. **Detection**: Identify audio file references in markdown
2. **Format Support**: Check format support for target output
3. **Embedding**: Embed in PowerPoint, link in Word/PDF
4. **Fallback**: Use placeholder with link if embedding not possible

#### Audio Format Support

- **PowerPoint**: MP3, WAV, M4A (format-dependent)
- **Word/PDF**: Link to audio file (no embedding)

### Other Media Types

#### Handling Strategy

1. **Detection**: Identify media file references
2. **Format Check**: Check if format is supported
3. **Fallback**: Use placeholder or skip if not supported
4. **Logging**: Log unsupported media types

## Error Handling

### Missing Images

#### Detection

- **Path Resolution**: Attempt to resolve image path
- **File Check**: Check if file exists at resolved path
- **Error**: Mark as missing if file not found

#### Handling Strategy

1. **Placeholder**: Insert placeholder text "[Image: alt text - file not found]"
2. **Logging**: Log warning with image path and alt text
3. **Continuation**: Continue conversion process
4. **User Notification**: Optionally notify user of missing images

#### Placeholder Format

- **Text**: "[Image: {alt text} - file not found]"
- **Styling**: Italic, gray color (#8A8886)
- **Size**: Same as surrounding text
- **Position**: At image reference location

### Broken Image References

#### Detection

- **Syntax Check**: Validate markdown image syntax
- **Path Validation**: Validate image path format
- **Error**: Mark as broken if syntax invalid

#### Handling Strategy

1. **Skip**: Skip invalid image references
2. **Logging**: Log error with reference details
3. **Continuation**: Continue conversion process
4. **User Notification**: Optionally notify user of broken references

### Unsupported Image Formats

#### Detection

- **Format Check**: Check if image format is supported
- **Conversion**: Attempt format conversion if possible
- **Error**: Mark as unsupported if conversion fails

#### Handling Strategy

1. **Conversion**: Attempt to convert to supported format
2. **Fallback**: Use placeholder if conversion fails
3. **Logging**: Log warning for unsupported formats
4. **Continuation**: Continue conversion process

### Network Image References

#### Handling Strategy

1. **URL Validation**: Validate image URL format
2. **Download**: Attempt to download image from URL
3. **Embedding**: Embed downloaded image
4. **Fallback**: Use placeholder if download fails

#### Download Considerations

- **Timeout**: Set download timeout (30 seconds default)
- **Size Limit**: Set maximum download size (10MB default)
- **Caching**: Cache downloaded images for reuse
- **Error Handling**: Handle network errors gracefully

## Path Resolution

### Relative Paths

#### Resolution Strategy

1. **Base Path**: Use markdown file directory as base path
2. **Path Joining**: Join base path with relative image path
3. **Normalization**: Normalize path (resolve `..`, `.`, etc.)
4. **Validation**: Validate resolved path exists

#### Examples

- **Markdown File**: `/documents/report.md`
- **Image Reference**: `![alt](images/photo.png)`
- **Resolved Path**: `/documents/images/photo.png`

### Absolute Paths

#### Resolution Strategy

1. **Path Validation**: Validate absolute path format
2. **File Check**: Check if file exists at absolute path
3. **Access Check**: Verify file is accessible
4. **Usage**: Use absolute path as-is

#### Examples

- **Image Reference**: `![alt](/images/photo.png)`
- **Resolved Path**: `/images/photo.png` (Unix) or `C:\images\photo.png` (Windows)

### URL References

#### Resolution Strategy

1. **URL Validation**: Validate URL format
2. **Protocol Check**: Support HTTP and HTTPS
3. **Download**: Download image from URL
4. **Cache**: Cache downloaded image locally

#### Examples

- **Image Reference**: `![alt](https://example.com/image.png)`
- **Action**: Download from URL and embed

## Implementation Notes

### Image Processing Libraries

#### JavaScript/TypeScript Options

- **Sharp**: High-performance image processing
- **Jimp**: Pure JavaScript image processing
- **Canvas**: HTML5 Canvas for image manipulation

#### Python Options

- **Pillow (PIL)**: Comprehensive image processing
- **OpenCV**: Advanced image processing (if needed)
- **Wand**: ImageMagick binding

### Performance Considerations

1. **Lazy Loading**: Load images only when needed
2. **Caching**: Cache processed images
3. **Parallel Processing**: Process multiple images in parallel
4. **Memory Management**: Manage memory for large images

### Quality vs. File Size

1. **Balance**: Balance image quality and file size
2. **Compression**: Apply appropriate compression
3. **Resolution**: Use appropriate resolution for format
4. **Format Selection**: Choose format based on image type

## Conclusion

This media handling specification provides comprehensive rules for processing, optimizing, and embedding images and media files in Word, PowerPoint, and PDF formats. By following these rules, the conversion tool will properly handle all media types, optimize for file size and quality, and ensure consistent presentation across all output formats.

