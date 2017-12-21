# Welcome to the Documentation
    This documentation needs to be kept alive to be useful. 
    So please, keep it maintained!

## Quick Questions and Answers

###*** How do I install the documentation system locally? ***

Go to the top-level `docs` directory in your repository.
Run `setup.py` and it should install itself for you.

###*** How do I add a page?***

If you want to add a page goto the relevant directory in the repository and add a `docs` folder.
Inside that docs folder add your markdown text, the filename should end with: `.md`
If the docs folder already exist, create the file inside that folder.

Run the `update_documentation.py` in the top-level docs directory and the documentation will be regenerated.
By default these files are created in /tmp/build for you.

This is something you can change by updating the path in the `config.yaml` file which also can be found in the top-level `docs` directory.

> Note: always put build files outside of the repository, or the script will iterate on itself and bad things will happen.

###*** How do I view the documentation? ***

There are two ways to view the documentation.

_Locally:_

In the build directory, after an `update_documentation.py`, run:
`mkdocs serve`

This will start a local webserver for you, showing you the documentation on `localhost:8000`

_Externally:_

TeamCity has a trigger to rebuild the documentation whenever something is merged to staging.

---

## Reference

To get started with markdown, [here is a simple tutorial](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

For simpler editing both for Windows and Linux, use a tool such as [Remarkable](https://remarkableapp.github.io)

---


