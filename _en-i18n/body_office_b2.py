def main():
    # ---------------- mindmap (20) ----------------
    write('mindmap', build('mindmap', [
        "👀 Mind Map Editor",
        "Write the hierarchy on the left using Markdown indentation and see the mind map generated live on the right, with zoom, drag and export support.",
        "/ Mind Map",
        "📖 Read the \"Mind Map Editor User Guide\"",
        "Markdown Editor",
        "Mind Map Preview",
        "⤢ Fit to Screen",
        "📚 Deep dive: Mind Map Editor",
        "When taking reading notes or brainstorming, express the hierarchy directly with # headings and indented - lists, and the mind map is generated automatically on the right, which is faster than drawing nodes by hand.",
        "When organizing meeting topics, put the central topic at level one and discussion points at child levels; the deeper the indent, the deeper the level, so the structure is clear at a glance.",
        "When preparing a report outline, write the key points as a Markdown outline first and then export an image, using zoom, drag and node collapse/expand for the presentation.",
        "Example: write a mind map with indent syntax",
        "# Product Planning\n## User Growth\n- Channel Advertising\n- Event Referral\n## Experience Optimization\n- Performance\n- Interaction\n\nWrite on the left using indentation and the map is generated live on the right; scroll to zoom, drag to pan, and click a dot to collapse or expand child nodes. Click \"Fit to Screen\" before exporting PNG so the content displays fully.",
        "How do I adjust node levels?",
        "Use # for heading levels and - lists for child nodes; the more indentation, the deeper the level. The Tab key quickly indents to adjust subordination.",
        "How do I export the complete mind map?",
        "Export to SVG and PNG is supported; before exporting PNG, click \"Fit to Screen\" first to make sure all content falls inside the canvas without being cut off. Drafts are stored in localStorage.",
        "About \"Mind Map Editor\"",
        "# Topic\n## Branch 1\n- Child node\n## Branch 2",
        "Fit to Screen",
    ]))

    # ---------------- pdf-merge (16) ----------------
    write('pdf-merge', build('pdf-merge', [
        "🔀 PDF Merge Tool",
        "Select multiple PDF files, drag to reorder them, then merge them with one click. All processing happens locally in your browser and files are never uploaded to the server.",
        "/ PDF Merge Tool",
        "📖 Read the \"PDF Merge Tool User Guide\"",
        "🔀 Merge All PDFs",
        "📚 Deep dive: PDF Merge Tool",
        "Merge several scattered contracts or scans into one file in order, making unified archiving and sending easier.",
        "When submitting application materials, stitch the cover, body and appendices in table-of-contents order so page order does not get mixed up.",
        "When tidying up meeting minutes, merge multi-page image-based PDFs into a single document to reduce the file count and ease searching.",
        "Example: merge three files in a given order",
        "Add \"cover.pdf, body.pdf, appendix.pdf\" in sequence; the top-to-bottom order of the list is the page order after merging (numbers ①②③). Reorder with drag or the move up / move down buttons; encrypted or corrupted files are skipped with a notice and do not affect the rest. Processing happens locally in your browser and files are never uploaded to the server.",
        "How is page order determined after merging?",
        "The merge order is the top-to-bottom order of the file list, where numbers ①②③ correspond to pages 1, 2 and 3 of the merged document; use drag or move up / move down to fine-tune it.",
        "Can encrypted or corrupted PDFs be merged?",
        "Encrypted or corrupted files are skipped automatically with a notice and do not affect the other valid files; decrypt or repair them first before adding them.",
        "About \"PDF Merge Tool\"",
    ]))

    # ---------------- pdf-rotate (17) ----------------
    write('pdf-rotate', build('pdf-rotate', [
        "🖼️ PDF Page Rotate Tool",
        "Rotate PDF page orientation entirely in the browser, supporting single-page, batch and rotate-all modes with live preview, and files are never uploaded to the server.",
        "/ PDF Page Rotate",
        "📖 Read the \"PDF Page Rotate Tool User Guide\"",
        "Selected",
        "pages",
        "📚 Deep dive: PDF Page Rotate Tool",
        "When scanned pages have inconsistent orientation (mixed landscape and portrait), rotate page by page or in batch to the correct direction for easier reading and printing.",
        "When an entire document is upside down, use the \"Rotate All\" mode to correct it in one go.",
        "When only some pages are oriented wrongly, use \"Rotate Single Page\" to fine-tune them without touching the rest.",
        "Example: straighten landscape-scanned pages",
        "Select the target pages and click \"Rotate Left 90°\" or \"Rotate Right 90°\"; the thumbnail previews the rotation live and shows the current angle. Three modes are supported - single page, batch and rotate all - and you can reset to the original orientation with one click. Rotation only changes page orientation and never modifies text or image content.",
        "Does rotating change the original content?",
        "No. Rotation only changes page orientation (the visual angle); text, images and other content stay identical, and you can reset to the original orientation at any time with one click.",
        "Which rotation modes are supported?",
        "Three modes are provided - single page, batch and rotate all - so you can fine-tune page by page or correct the whole document; generating thumbnails for a large file may take a few seconds, so please be patient.",
        "About \"PDF Page Rotate Tool\"",
    ]))

    # ---------------- pdf-split (21) ----------------
    write('pdf-split', build('pdf-split', [
        "🔀 PDF Split Tool",
        "Upload a PDF and extract the pages you want by page range or visual selection to build a new PDF. All processing happens locally in your browser and files are never uploaded.",
        "/ PDF Split Tool",
        "📖 Read the \"PDF Split Tool User Guide\"",
        "📋 Range Input",
        "👁️ Visual Selection",
        "Supported formats: a single page number (such as",
        "), a continuous range (such as",
        "), or comma-separated segments (such as",
        "📚 Deep dive: PDF Split Tool",
        "Extract the signature page or a specific chapter from a large contract and send it separately.",
        "Use a page range like \"1-3, 5, 7-10\" to quickly cut out several non-contiguous pages.",
        "Use the visual thumbnail selection to pick the pages you want to keep, with WYSIWYG results.",
        "Example: split by page range",
        "Enter \"1-3, 5, 7-10\" in the page range box and the tool extracts those pages in that order into a new PDF; you can also tick thumbnails directly, with one-click select all / invert selection / odd-even page shortcuts. All processing happens locally in your browser and files are never uploaded to the server.",
        "How do I split non-contiguous pages?",
        "Describe the pages in the page range box with the format \"1-3, 5, 7-10\": a hyphen marks a continuous interval and commas separate segments, and the extraction order equals the order you type them in.",
        "Can encrypted PDFs be split?",
        "Encrypted / password-protected PDFs allow the page count and thumbnails to be read, but page extraction may be restricted; remove the protection first. Generating thumbnails for files over 50 pages may take a few seconds.",
        "About \"PDF Split Tool\"",
        "For example: 1-3, 5, 7-10",
    ]))


if __name__ == '__main__':
    main()
