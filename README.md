# SUURPh-summer-school

This is the web-page of the Simula Summer School in Computational Physiology

## Add section to web-page

To add a notebook or markdown document to the web-page, please open [\_toc.yml](_toc.yml), create a new section if needed and add the file-name (without file extension)

## Hide input/output for students

If you want to hide a cell (input) or the data produce by a cell (output), you can use `pre-commit` to collapse these in the jupyter notebook.
They will be collapsed on the jupyter-server (that uses jupyter-lab), and will be collapsed on the webpage.
Simply add the tags `hide-input` and/or `hide-output` to the cell tag in the Jupyter notebook.

To enforce this you can run `pre-commit` in the repository:

```bash
python3 -m pip install pre-commit
pre-commit autoupdate
pre-commit run
```

This will update the appropriate meta-data in the files (which in turn can be commited).
If you have any questions or issues with this, please contact [Jørgen S. Dokken](https://github.com/jorgensd/) or make an [issue](https://github.com/Simula-SSCP/SSCP_2024_lectures/issues/new).
