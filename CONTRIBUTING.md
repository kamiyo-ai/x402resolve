# Contributing

## Code of Conduct

- Respectful, constructive discussion
- Assist newcomers
- Focus on project goals
- Professional conduct

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- Rust + Anchor CLI
- Solana CLI
- Git

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/x402resolve.git
   cd x402resolve
   ```

3. Set up the development environment:
   ```bash
   # Install TypeScript SDK dependencies
   cd packages/x402-sdk
   npm install

   # Install Python dependencies
   cd ../x402-verifier
   pip install -r requirements.txt
   pip install -r requirements-dev.txt

   # Build Solana program
   cd ../x402-escrow
   anchor build
   ```

4. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/x402kamiyo/x402resolve.git
   ```

## How to Contribute

### Reporting Bugs

Before filing:
1. Check existing issues
2. Collect: OS, versions, error messages
3. Create minimal reproduction

Include:
- Descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Environment: OS, Node version
- Error logs/screenshots

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:

1. Check if the feature has already been requested
2. Clearly describe the use case and benefits
3. Provide examples or mockups if possible
4. Consider backwards compatibility

### Pull Requests

#### Before Submitting

1. Discuss major changes via an issue first
2. Update from the main branch:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

3. Test your changes thoroughly
4. Update documentation as needed
5. Add tests for new functionality

#### PR Guidelines

1. **Branch naming**: Use descriptive names:
   - `feature/add-multi-oracle-consensus`
   - `fix/escrow-time-lock-bug`
   - `docs/update-api-examples`

2. **Commit messages**: Follow conventional commits:
   ```
   type(scope): subject

   - feat: New feature
   - fix: Bug fix
   - docs: Documentation changes
   - test: Test additions/changes
   - refactor: Code refactoring
   - chore: Maintenance tasks
   ```

   Examples:
   - `feat(sdk): add reputation query method`
   - `fix(verifier): handle empty data edge case`
   - `docs(readme): update installation instructions`

3. **PR description**: Include:
   - What changes were made and why
   - Related issue numbers (closes #123)
   - Testing performed
   - Screenshots for UI changes
   - Breaking changes (if any)

4. **Code review**: Be responsive to feedback and ready to make changes

## Development Guidelines

### TypeScript (SDK)

- Use TypeScript strict mode
- Follow existing code style (ESLint + Prettier configured)
- Add JSDoc comments for public APIs
- Write unit tests for new functions
- Keep functions small and focused

Example:
```typescript
/**
 * Files a dispute for a transaction based on quality assessment
 * @param transactionId - The Solana transaction ID to dispute
 * @param evidence - Evidence supporting the dispute claim
 * @returns Promise resolving to dispute details
 */
async fileDispute(
  transactionId: string,
  evidence: DisputeEvidence
): Promise<DisputeResult> {
  // Implementation
}
```

### Python (Verifier Oracle)

- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings for classes and functions
- Add unit tests (pytest)
- Use async/await for I/O operations

Example:
```python
async def calculate_quality_score(
    query: str,
    data: dict,
    criteria: QualityCriteria
) -> QualityScore:
    """
    Calculate multi-factor quality score for API response data.

    Args:
        query: Original query string
        data: Response data to assess
        criteria: Quality assessment criteria

    Returns:
        QualityScore with semantic, completeness, and freshness metrics
    """
    # Implementation
```

### Rust (Solana Program)

- Follow Rust conventions and idioms
- Use `anchor-lang` best practices
- Add comprehensive error types
- Write integration tests
- Document security considerations

Example:
```rust
/// Resolves a dispute by executing the refund split based on verified quality score
#[access_control(verify_oracle_signature(&ctx, quality_score, &signature))]
pub fn resolve_dispute(
    ctx: Context<ResolveDispute>,
    quality_score: u8,
    signature: [u8; 64]
) -> Result<()> {
    // Implementation
}
```

### Testing

All contributions should include appropriate tests:

- **Unit tests**: Test individual functions/methods
- **Integration tests**: Test component interactions
- **End-to-end tests**: Test complete workflows

Run tests before submitting:
```bash
# TypeScript tests
cd packages/x402-sdk
npm test

# Python tests
cd packages/x402-verifier
pytest

# Rust tests
cd packages/x402-escrow
anchor test
```

### Documentation

- Update README.md for user-facing changes
- Add/update inline code documentation
- Update API documentation in `/docs`
- Include examples for new features
- Check spelling and grammar

## Project Structure

```
x402resolve/
├── packages/
│   ├── x402-sdk/          # TypeScript client library
│   ├── x402-verifier/     # Python quality oracle
│   ├── x402-escrow/       # Rust Solana program
│   └── mcp-server/        # MCP protocol server
├── examples/              # Integration examples
├── docs/                  # Technical documentation
└── tests/                 # Integration tests
```

## Areas for Contribution

We welcome contributions in these areas:

### High Priority

- Multi-oracle consensus implementation (Phase 2)
- Additional quality scoring metrics
- Performance optimizations
- Security improvements
- Additional integration examples

### Good First Issues

- Documentation improvements
- Test coverage expansion
- Error message improvements
- Code comments and clarity
- Example applications

### Advanced Features

- Cross-chain escrow support (Ethereum, BSC)
- Machine learning quality models
- Real-time monitoring dashboard
- Advanced reputation algorithms
- Governance mechanisms

## Security Considerations

When contributing:

1. **Never commit secrets**: Use environment variables
2. **Validate all inputs**: Especially in Solana program
3. **Consider attack vectors**: Time locks, overflow, reentrancy
4. **Document security assumptions**: In code and PRs
5. **Report vulnerabilities privately**: See SECURITY.md

## Review Process

1. Automated checks must pass (tests, linting)
2. At least one maintainer review required
3. Address all review feedback
4. Maintainer will merge approved PRs

## Release Process

- Semantic versioning (MAJOR.MINOR.PATCH)
- Release notes for each version
- Breaking changes clearly documented
- Migration guides when needed

## Getting Help

- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and ideas
- Documentation: See `/docs` directory
- Examples: See `/examples` directory

## Recognition

Contributors are recognized in:

- GitHub contributors page
- Release notes for significant contributions
- Project README (major features)

## License

By contributing to x402Resolve, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to x402Resolve! Your efforts help make automated dispute resolution better for everyone.
