# E-document Evidence Gathering & Investigation(EEGI)

## INTRODUCTION

We implemented a tool for EEGI using the open-source tool, which is based on Python. The figure illustrates the overall structure of EEGI, and ESIS, and is available on GitHub. Firstly, this tool takes forensic images as input and analyzes the filesystem to examine the list and metadata of files. This tool is divided into LV1 and LV2 modules. LV1 modules consist of artifact-based analysis code, and LV2 modules utilize the analysis results from LV1 modules to perform deeper analysis. We implemented ESIS as one of the LV2 modules, incorporating preprocessed datasets as well.


##### Other information
Release: 
Dataset: 

# How to build?

## Windows

## Python
To build EEGI, The Python 3.7.x is required.

The Python 3.7.x must be registered in the system environment variable.

## Visual Studio Community 2019
Download from: https://visualstudio.microsoft.com/ko/vs/features/cplusplus/

And, install "Desktop development with C++"

## Install EEGI

To run EEGI, We must change PowerShell Execution Policy.

Execute PowerShell as administrator:
<pre><code>Set-ExecutionPolicy Unrestricted</code></pre>

And enter
<pre><code>A</code></pre>

Installing the requirements library to run EEGI in PowerShell:
<pre><code>.\build.ps1</code></pre>


# How to execute?

<pre><code>EEGI.exe [source] [output] --cid [case_name] --eid [evidence_name] -z [time_zone] --sqlite
</code></pre>

<pre><code>EEGI.exe [source] [output] --modules [module_name,...] --advanced_modules [advanced_module_name,...] --cid [case_name] --eid [evidence_name] -z [time_zone] --sqlite
</code></pre>

The time zone can be obtained from the 'TZ identifier' in the URL below.
- https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

<pre><code>python main.py [source] [output] --cid [case_name] --eid [evidence_name] -z [time_zone] --sqlite
</code></pre>

<pre><code>python main.py [source] [output] --modules [module_name,...] --advanced_modules [advanced_module_name,...] --cid [case_name] --eid [evidence_name] -z [time_zone] --sqlite
</code></pre>

Now, We support these modules.
<pre><code>thumbnailcache_connector,searchdb_connector,shellbag_connector,stickynote_connector,windows_timeline_connector,ntfs_connector,eventlog_connector,chromium_connector,filehistory_connector,jumplist_connector,link_connector,esedb_connector,iconcache_connector,recyclebin_connector,registry_connector,prefetch_connector,defa_connector/xls,defa_connector/doc,defa_connector/ppt,defa_connector/hwp,defa_connector/docx,defa_connector/xlsx,defa_connector/pptx,defa_connector/pdf,email_connector</code></pre>

Now, We support these advanced modules.
<pre><code>lv2_document_classifier,lv2_os_app_history_analyzer,lv2_os_mft_history_analyzer,lv2_os_log_history_analyzer</code></pre>

## Result

The output of ESIS can be found in the output sqlite file in the 'lv2_document_classifier' table.
