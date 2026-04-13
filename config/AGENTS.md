<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-13 | Updated: 2026-04-13 -->

# config

## Purpose
Project configuration files for the Vitruvius pipeline.

## Key Files
| File | Description |
|------|-------------|
| `vitruvius.yaml` | Main project configuration (categories, paths, version) |

## For AI Agents

### Working In This Directory
- All configuration is in YAML format
- Config defines the 9 knowledge categories
- Path settings map layer names to folder names

### Testing Requirements
- Verify YAML parses correctly
- Check category names match layer folder names

### Common Patterns
- Single config file for simplicity
- Categories: 001-Laws through 009-Practice

## Dependencies

### External
- `PyYAML` - Configuration parsing

<!-- MANUAL: -->