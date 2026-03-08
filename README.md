# RTL Productivity and CI/CD Toolkit

A small reproducible RTL execution backbone for smoke runs, regressions, triage, and report generation.

## Goal

Create a repeatable repository structure and command flow so every RTL project can be:
- run the same way every time
- debugged from saved artifacts
- summarized with simple reports
- resumed after a break without depending on shell history

This repo is the backbone for later RTL projects.

## Current status

Current supported simulator path:
- XSIM via Vivado / Xilinx tools in PATH

Current implemented flow:
- single smoke run
- regression wrapper
- triage classification
- markdown summary report

## Repository structure

```text
rtl/        RTL source files
tb/         Testbench source files
scripts/    Run, regress, triage, report scripts
docs/       Command notes and restart instructions
reports/    Generated run artifacts
evidence/   Screenshots / proof material you want to keep
tests.yaml  Test list configuration