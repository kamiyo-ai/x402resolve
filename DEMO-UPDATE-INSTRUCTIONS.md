# Demo Site Update Instructions

## Current Status

✓ **Program Deployed**: E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n (devnet)
✓ **Code Updated**: docs/oracle-transactions.js has correct program ID
✓ **HTML Updated**: docs/index.html now references oracle-transactions.js
✗ **Live Site**: Still showing old program ID (needs deployment)

## Files Updated

1. **docs/index.html** - New file added
   - References `oracle-transactions.js` (not timestamped version)

2. **docs/oracle-transactions.js** - Already correct
   - Line 6: `const PROGRAM_ID = 'E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n';`

## To Update Live Demo at https://x402resolve.kamiyo.ai/

### Option 1: Push to kamiyo-ai/x402resolve (Recommended)

```bash
# Pull latest changes from your fork
cd /path/to/kamiyo-ai-x402resolve-clone

# Add your fork as remote if not already
git remote add fork https://github.com/x402kamiyo/x402resolve.git

# Pull the demo updates
git pull fork main

# Push to kamiyo-ai (you have access, I don't)
git push origin main
```

### Option 2: Create Pull Request

1. Go to https://github.com/x402kamiyo/x402resolve
2. Click "Contribute" → "Open pull request"
3. Title: "Update demo to use new deployed program"
4. Merge the PR

### Option 3: Manual Update

If you have the kamiyo-ai/x402resolve repo locally:

```bash
cd /path/to/kamiyo-ai/x402resolve

# Copy updated files
cp /Users/dennisgoslar/Projekter/kamiyo-x402resolve/docs/index.html docs/
cp /Users/dennisgoslar/Projekter/kamiyo-x402resolve/docs/oracle-transactions.js docs/

# Commit and push
git add docs/
git commit -m "Update demo to use deployed program E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n"
git push origin main
```

## Enable GitHub Pages (if not already enabled)

1. Go to https://github.com/kamiyo-ai/x402resolve/settings/pages
2. Source: Deploy from a branch
3. Branch: main
4. Folder: /docs
5. Save

## Verify Deployment

After pushing, wait 1-2 minutes for GitHub Pages to rebuild, then:

```bash
# Check the JS file has correct program ID
curl -s https://x402resolve.kamiyo.ai/oracle-transactions.js | grep "PROGRAM_ID = "

# Should output:
# const PROGRAM_ID = 'E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n';
```

## What Changed

**Before:**
- Demo HTML referenced timestamped file: `oracle-transactions-20251108191536.js`
- That file had old program ID: `AFmBBw7kbrnwhhzYadAMCMh4BBBZcZdS3P7Z6vpsqsSR`

**After:**
- Demo HTML references: `oracle-transactions.js`
- That file has new program ID: `E5EiaJhbg6Bav1v3P211LNv1tAqa4fHVeuGgRBHsEu6n`
- Matches the newly deployed program on devnet
