# Preparing an NIH grant proposal using LaTeX

The NIH has [very specific guidelines](https://grants.nih.gov/grants/funding/phs398/phs398.html) for preparing a grant proposal, and getting those guidelines implemented in LaTeX is somewhat non-trivial. For my own future reference and to help others who may want to submit NIH grants in LaTeX format, I am providing [this template](https://github.com/Noble-Lab/nih-latex/blob/main/nih-r01.tex). Using [this simple makefile](https://github.com/Noble-Lab/nih-latex/blob/main/makefile) produces an empty document that looks like [this](https://github.com/Noble-Lab/nih-latex/blob/main/nih-r01.pdf). I have used this form to successfully submit multiple grant proposals to the NIH, so I feel somewhat confident that it accurately implements the NIH guidelines.

Here are some notes regarding the template:

-    The NIH requires that the various pieces of the grant be uploaded separately. I find it easiest to produce a single PDF in LaTeX, then break it into separate pieces just before submission.

-    While writing the grant, I typically embed the actual instructions for each section into the document. When it's time to submit (or when I need to check on the length restriction), I uncomment the "instructions" line in the header of the file.

-    When submitting a revised grant, the sections that have been modified need to be indicated in the proposal. I typically do this by inserting the following lines into the header of the document:

```
    % In the revised version, we will use changebars to indicate where the
    % text has been modified.  Use ``\cbstart{foo foo foo \cbend}'' to
    % delimit these areas.
    % For documentation, see 
    % http://www.ctan.org/tex-archive/macros/latex/contrib/changebar/changebar.pdf
    \usepackage[rightbars]{changebar}

    % Make the changebar close to the text.
    \setlength{\changebarsep}{0.05in}
    \setlength{\changebarsep}{0.05in}

    % Use 1/2-inch margins.
    % Include extra space on right for the changebars.
    \usepackage[left=0.5in,top=0.5in,bottom=0.5in,right=0.6in]{geometry}
```

Other NIH+Latex web pages:

- [Using LaTeX for NIH Grant Applications](https://users.cs.duke.edu/~brd/NIH/tips/)

I would welcome any comments or suggestions for improvement to the above template.

Bill Noble
william-noble@uw.edu
