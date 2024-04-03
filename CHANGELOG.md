# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

# Nuclei Analysis Automation Task

## [Unreleased]

## [0.0.0] - [Unreleased] 2023-12-27 [Patched] 2024-03-23

## Added:

- --titles features is added to enable analyst to give custom title even without using CTD
- A progressbar is added for listing vulnerability check in platform
- HTTP Response is printed whenever a exception is related to HTTP Parsing for Debug  purpose  
- User can either select existing scanner or create Default scanners risksense and risksense app
- Exploit Name used from titles is now printed in UI

## Changed

- Scanneruuid used to create vulnerability is dynamic now and a search & create feature is added to support the smooth flow

# Fixed

- Patched the issue with title containing dot, causing template search and figure description issue 
- Handling scenario where titles are not required for certain issues
- In weird cases APPID is set to None, to handle it we are raising a keyerror
- Ctrl+C in verification of created vulnerability is fixed and does not exist rather skips the step now
- Create scanner logic is fixed in case a incompatible scanner type is found 

## [3.0.3] - [Unreleased] 2023-07-17 

## Fixed:
- Optimized the meta issue in the cherrytree regex, hence CVSSv3.1 Vector can be above Description. This also Fixes unnecessary key pair values generated while parsing.


## [3.0.2] - [Unreleased] 2023-05-31 

## Added:
- Added new logic to parse port and service in accordance to hostname/ip
- json supports the same port and service logic
- added argument for version 
- Added cherrytree 00.99.40 exe to project

## Changed
- Hostfinding creation logic is updated to create each finding one by one instead of creating all findings in a single go to support port and service mapping

## Fixed
- data issue in hostsearch
- Handled exception if data is missing in parent node
- Port and service error handling patch
- Handled exception raised in create vuln print statement


## [3.0.1] - [Unreleased] 2023-05-23 - [Patched] - 2023-05-30

## Added
- using src folder scripts such as ctd_html_parser.py and net_parser.py from uctexploit3
- Supports ctd for both network and web
- Supports data.json as input is more stable
- Multiple instance of the same vulnerability is created based on provided urls

## Changed
- Restructed the code structure and ui
- Images are Files are not stored in physical path instead its stored as base64 in memory
- Removed Exploiteater from here
- Comparsion for ['CWE','Other','host','URL','Port'] is based on list
- For severity change note, keyword is 'reason' instead of note

## Fixed
- Removed invalid if condition for cherrytree
- Add if condition in ctd_html_parser to update url only for app projects
- fixed hostsearch and createvuln instance issue
- fixed change severity issue in hostfindings
- fixed html entity encoding issue



