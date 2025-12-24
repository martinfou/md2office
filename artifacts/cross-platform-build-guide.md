# Cross-Platform Build Guide

## Overview

This guide defines the build strategy for creating portable, self-contained binary executables for Windows and Mac. The build process ensures that the tool can be distributed as a single executable file that works without installation or external dependencies.

### Build Goals

1. **Portability**: Single executable file per platform
2. **Self-Contained**: All dependencies bundled in executable
3. **No Installation**: Run directly without installation
4. **Cross-Platform**: Support Windows and Mac (Intel and Apple Silicon)
5. **Performance**: Fast startup and execution

### Build Philosophy

- **Single Binary**: One executable file per platform
- **Static Linking**: Statically link dependencies where possible
- **Dependency Bundling**: Bundle all required libraries and resources
- **Minimal Runtime**: No external runtime dependencies
- **Cross-Compilation**: Build for multiple platforms from single codebase

## Build Toolchain Options

### Option 1: Go (Recommended)

#### Advantages

- **Single Binary**: Compiles to single executable
- **Cross-Compilation**: Easy cross-compilation for multiple platforms
- **Static Linking**: Statically links dependencies
- **Fast Execution**: Fast startup and execution
- **Good Libraries**: Good libraries for document generation

#### Build Tools

- **Go Compiler**: Standard Go toolchain
- **Build Flags**: `-ldflags` for embedding resources
- **Cross-Compilation**: `GOOS` and `GOARCH` environment variables

#### Example Build Commands

```bash
# Windows 64-bit
GOOS=windows GOARCH=amd64 go build -o md2office.exe

# macOS Intel
GOOS=darwin GOARCH=amd64 go build -o md2office

# macOS Apple Silicon
GOOS=darwin GOARCH=arm64 go build -o md2office
```

### Option 2: Rust

#### Advantages

- **Single Binary**: Compiles to single executable
- **Cross-Compilation**: Good cross-compilation support
- **Static Linking**: Statically links dependencies
- **Performance**: Excellent performance
- **Memory Safety**: Memory-safe language

#### Build Tools

- **Cargo**: Rust package manager and build tool
- **Cross**: Cross-compilation tool
- **Musl**: Static linking with musl libc

#### Example Build Commands

```bash
# Windows 64-bit
cargo build --release --target x86_64-pc-windows-gnu

# macOS Intel
cargo build --release --target x86_64-apple-darwin

# macOS Apple Silicon
cargo build --release --target aarch64-apple-darwin
```

### Option 3: Python with PyInstaller

#### Advantages

- **Rapid Development**: Fast development cycle
- **Rich Libraries**: Excellent libraries for document generation
- **Cross-Platform**: Works on Windows and Mac
- **Single Executable**: PyInstaller creates single executable

#### Disadvantages

- **Larger Binaries**: Larger executable size
- **Slower Startup**: Slower startup time
- **Dependency Management**: More complex dependency bundling

#### Build Tools

- **PyInstaller**: Creates standalone executables
- **cx_Freeze**: Alternative to PyInstaller
- **Nuitka**: Compiles Python to C++

#### Example Build Commands

```bash
# Windows
pyinstaller --onefile --name md2office md2office.py

# macOS
pyinstaller --onefile --name md2office md2office.py
```

### Option 4: JavaScript/TypeScript with pkg

#### Advantages

- **Rapid Development**: Fast development cycle
- **Rich Ecosystem**: Excellent npm packages
- **Cross-Platform**: Works on Windows and Mac

#### Disadvantages

- **Larger Binaries**: Larger executable size
- **Node.js Runtime**: Bundles Node.js runtime

#### Build Tools

- **pkg**: Packages Node.js apps into executables
- **nexe**: Alternative to pkg
- **electron-builder**: For Electron apps (larger)

#### Example Build Commands

```bash
# Build for all platforms
pkg package.json --targets node18-win-x64,node18-macos-x64,node18-macos-arm64
```

## Recommended Approach: Go

### Rationale

1. **Single Binary**: Go compiles to single executable
2. **Cross-Compilation**: Easy cross-compilation
3. **Static Linking**: Statically links dependencies
4. **Performance**: Fast startup and execution
5. **Good Libraries**: Good libraries for document generation

### Build Setup

#### Project Structure

```
md2office/
├── cmd/
│   └── md2office/
│       └── main.go
├── internal/
│   ├── converter/
│   ├── parser/
│   └── generator/
├── go.mod
├── go.sum
└── build.sh
```

#### Build Script

```bash
#!/bin/bash

# Build for Windows 64-bit
echo "Building for Windows 64-bit..."
GOOS=windows GOARCH=amd64 go build -ldflags="-s -w" -o dist/md2office-windows-amd64.exe ./cmd/md2office

# Build for macOS Intel
echo "Building for macOS Intel..."
GOOS=darwin GOARCH=amd64 go build -ldflags="-s -w" -o dist/md2office-darwin-amd64 ./cmd/md2office

# Build for macOS Apple Silicon
echo "Building for macOS Apple Silicon..."
GOOS=darwin GOARCH=arm64 go build -ldflags="-s -w" -o dist/md2office-darwin-arm64 ./cmd/md2office

echo "Build complete!"
```

## Platform-Specific Builds

### Windows Build

#### Target Specifications

- **Platform**: Windows 10+ (64-bit)
- **Architecture**: x86_64 (AMD64)
- **Binary Format**: .exe (PE executable)
- **Minimum Windows Version**: Windows 10

#### Build Requirements

- **Go Version**: Go 1.21 or later
- **CGO**: May require CGO for some libraries (set `CGO_ENABLED=0` for static linking)
- **Cross-Compiler**: Use Go's built-in cross-compilation

#### Build Command

```bash
# Windows 64-bit
GOOS=windows GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o md2office.exe ./cmd/md2office
```

#### Binary Characteristics

- **File Extension**: .exe
- **Format**: PE (Portable Executable)
- **Size**: ~10-20 MB (depending on dependencies)
- **Dependencies**: Statically linked, no external DLLs required

### macOS Build

#### Target Specifications

- **Platform**: macOS 10.15+ (Catalina and later)
- **Architecture**: 
  - Intel: x86_64
  - Apple Silicon: arm64
- **Binary Format**: Mach-O executable
- **Universal Binary**: Optional universal binary (Intel + Apple Silicon)

#### Build Requirements

- **Go Version**: Go 1.21 or later
- **macOS SDK**: May require macOS SDK for some features
- **Code Signing**: Optional code signing for distribution

#### Build Commands

```bash
# macOS Intel
GOOS=darwin GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o md2office-darwin-amd64 ./cmd/md2office

# macOS Apple Silicon
GOOS=darwin GOARCH=arm64 CGO_ENABLED=0 go build -ldflags="-s -w" -o md2office-darwin-arm64 ./cmd/md2office

# Universal Binary (requires lipo)
# Build both architectures first, then combine:
lipo -create md2office-darwin-amd64 md2office-darwin-arm64 -output md2office-darwin-universal
```

#### Binary Characteristics

- **File Extension**: None (Unix executable)
- **Format**: Mach-O
- **Size**: ~10-20 MB (depending on dependencies)
- **Dependencies**: Statically linked, no external libraries required
- **Permissions**: Executable permission set

## Dependency Bundling

### Static Linking Strategy

#### Go Dependencies

- **Static Linking**: Go statically links dependencies by default
- **CGO Disabled**: Set `CGO_ENABLED=0` for pure Go static linking
- **External Libraries**: Use pure Go libraries when possible

#### External Libraries

For libraries that require C dependencies:

1. **Static Linking**: Link C libraries statically
2. **Bundle Libraries**: Bundle required libraries with executable
3. **Pure Go Alternatives**: Prefer pure Go alternatives when available

### Resource Embedding

#### Embedding Resources

**Go 1.16+ embed directive**:

```go
//go:embed templates/*.html
var templates embed.FS

//go:embed fonts/*
var fonts embed.FS
```

#### Configuration Files

- **Embed Default Config**: Embed default configuration in binary
- **External Config**: Allow external configuration file override
- **Resource Files**: Embed fonts, templates, and other resources

### Image Processing Libraries

#### Go Libraries

- **image/png, image/jpeg**: Standard library (pure Go)
- **github.com/disintegration/imaging**: Image processing (pure Go)
- **github.com/nfnt/resize**: Image resizing (pure Go)

#### Avoid C Dependencies

- Prefer pure Go image libraries
- Avoid libraries requiring ImageMagick or similar C libraries
- Use Go's standard image libraries when possible

### Document Generation Libraries

#### Word Generation

- **github.com/unidoc/unioffice**: Pure Go Word/Excel/PowerPoint library
- **github.com/lukasjarosch/go-docx**: Pure Go Word library

#### PDF Generation

- **github.com/jung-kurt/gofpdf**: Pure Go PDF library
- **github.com/signintech/gopdf**: Pure Go PDF library

#### PowerPoint Generation

- **github.com/unidoc/unioffice**: Pure Go PowerPoint library

## Binary Distribution

### Distribution Format

#### Single Executable

- **Windows**: `md2office.exe` (single file)
- **macOS**: `md2office` (single file)
- **No Installation**: No installer or setup required
- **Self-Contained**: All dependencies included

#### Distribution Package

**Windows**:
- Single .exe file
- Optional: ZIP archive with README

**macOS**:
- Single executable file
- Optional: DMG disk image with README

### File Size Optimization

#### Build Flags

```bash
# Strip debug symbols
-ldflags="-s -w"

# Disable CGO for static linking
CGO_ENABLED=0

# Optimize for size
-ldflags="-s -w -X main.version=1.0.0"
```

#### Compression

- **UPX**: Optional UPX compression (may trigger antivirus)
- **Native Compression**: Use Go's built-in compression
- **Resource Optimization**: Optimize embedded resources

### Code Signing (Optional)

#### Windows Code Signing

- **Certificate**: Code signing certificate required
- **signtool**: Use Windows SDK signtool
- **Timestamp**: Add timestamp server for long-term validity

#### macOS Code Signing

- **Developer ID**: Apple Developer ID certificate
- **codesign**: Use codesign tool
- **Notarization**: Optional notarization for Gatekeeper

## Testing Strategy

### Cross-Platform Testing

#### Build Testing

1. **Windows Build**: Test Windows build on Windows machine or CI
2. **macOS Build**: Test macOS build on macOS machine or CI
3. **Cross-Compilation**: Verify cross-compiled binaries work

#### Functional Testing

1. **Basic Conversion**: Test basic markdown conversion
2. **Format Testing**: Test Word, PowerPoint, PDF generation
3. **Error Handling**: Test error handling and edge cases
4. **Performance**: Test performance with large files

### CI/CD Integration

#### GitHub Actions Example

```yaml
name: Build

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [windows-latest, macos-latest]
        go-version: [1.21]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Go
      uses: actions/setup-go@v4
      with:
        go-version: ${{ matrix.go-version }}
    
    - name: Build
      run: |
        if [ "${{ matrix.os }}" == "windows-latest" ]; then
          go build -o md2office.exe ./cmd/md2office
        else
          go build -o md2office ./cmd/md2office
        fi
    
    - name: Test
      run: go test ./...
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: md2office-${{ matrix.os }}
        path: md2office*
```

## Build Automation

### Makefile

```makefile
.PHONY: build build-windows build-macos clean

build: build-windows build-macos

build-windows:
	@echo "Building for Windows..."
	GOOS=windows GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/md2office-windows-amd64.exe ./cmd/md2office

build-macos-intel:
	@echo "Building for macOS Intel..."
	GOOS=darwin GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/md2office-darwin-amd64 ./cmd/md2office

build-macos-arm:
	@echo "Building for macOS Apple Silicon..."
	GOOS=darwin GOARCH=arm64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/md2office-darwin-arm64 ./cmd/md2office

build-macos: build-macos-intel build-macos-arm
	@echo "Creating universal binary..."
	lipo -create dist/md2office-darwin-amd64 dist/md2office-darwin-arm64 -output dist/md2office-darwin-universal

clean:
	rm -rf dist/

test:
	go test ./...
```

### Build Scripts

#### build.sh (Unix/macOS)

```bash
#!/bin/bash

set -e

echo "Building md2office..."

# Create dist directory
mkdir -p dist

# Build for Windows
echo "Building for Windows 64-bit..."
GOOS=windows GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/md2office-windows-amd64.exe ./cmd/md2office

# Build for macOS Intel
echo "Building for macOS Intel..."
GOOS=darwin GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/md2office-darwin-amd64 ./cmd/md2office

# Build for macOS Apple Silicon
echo "Building for macOS Apple Silicon..."
GOOS=darwin GOARCH=arm64 CGO_ENABLED=0 go build -ldflags="-s -w" -o dist/md2office-darwin-arm64 ./cmd/md2office

echo "Build complete! Binaries in dist/ directory"
```

#### build.bat (Windows)

```batch
@echo off

echo Building md2office...

mkdir dist 2>nul

echo Building for Windows 64-bit...
set GOOS=windows
set GOARCH=amd64
set CGO_ENABLED=0
go build -ldflags="-s -w" -o dist\md2office-windows-amd64.exe cmd\md2office\main.go

echo Build complete! Binaries in dist\ directory
```

## Implementation Notes

### Build Requirements

1. **Go Version**: Go 1.21 or later
2. **Cross-Compilation**: Go's built-in cross-compilation support
3. **Static Linking**: Use `CGO_ENABLED=0` for static linking
4. **Build Flags**: Use `-ldflags="-s -w"` for size optimization

### Dependency Management

1. **Go Modules**: Use Go modules for dependency management
2. **Vendor Directory**: Optional vendor directory for reproducible builds
3. **Version Pinning**: Pin dependency versions in go.mod
4. **Pure Go**: Prefer pure Go libraries when possible

### Performance Considerations

1. **Build Time**: Optimize build time with caching
2. **Binary Size**: Minimize binary size with build flags
3. **Startup Time**: Optimize startup time
4. **Memory Usage**: Optimize memory usage

## Conclusion

This cross-platform build guide provides comprehensive strategies for creating portable, self-contained binaries for Windows and Mac. The recommended approach using Go provides excellent cross-compilation support, static linking, and single-binary distribution. Following these guidelines will enable creation of portable executables that work without installation or external dependencies.

