# Exercise 5: Use AWS CLI with Claude to Download Hydrological Data

**Best practice:** Point Claude at an authenticated CLI tool and let it learn the tool itself — don't write API wrappers from scratch.

---

## What is the AWS CLI?

AWS (Amazon Web Services) is a cloud platform that hosts many large public datasets relevant to hydrology — NOAA's National Water Model, NEXRAD radar, ERA5 reanalysis, and USGS elevation data are all stored in AWS S3 (Simple Storage Service), which is essentially a massive file system in the cloud.

The **AWS CLI** (`aws`) is a command-line tool that lets you interact with S3 the same way you'd use File Explorer or Finder on your computer — browse folders, check file sizes, and download files — but from your terminal.

```bash
aws s3 ls   s3://some-bucket/folder/   # list files, like opening a folder
aws s3 cp   s3://some-bucket/file.nc . # download one file
aws s3 sync s3://some-bucket/folder/ . # download an entire folder
```

You don't need to write any Python or understand cloud APIs. Once the CLI is installed, these three commands cover the vast majority of data retrieval tasks.

## Why have Claude use the CLI directly?

When you ask Claude to "download data from AWS" without mentioning the CLI, it defaults to writing Python code using the `boto3` library — AWS's programmatic SDK. This works, but it has real drawbacks for a researcher:

| | boto3 Python code | AWS CLI |
|---|---|---|
| Setup | Requires AWS credentials configured in Python | Just `pip install awscli` |
| Bucket exploration | Claude must guess the folder structure | Claude runs `aws s3 ls` to discover it live |
| Safety | Downloads start immediately | `--dryrun` flag previews files before any data moves |
| Reusability | Script tied to one dataset | Same commands work on any S3 bucket |

The deeper reason: **Claude is highly proficient at reading `--help` output.** When you tell Claude to run `aws s3 ls --help` first, it learns the exact flags and syntax for your installed version of the CLI, then uses them correctly — no guessing, no version mismatches, no wrapper code to maintain.

---

## What you need

- AWS CLI installed (`pip install awscli`)
- No AWS account required — the NWM bucket is public

---

## Exercise

### Part A — Without CLI guidance

```
Download NWM retrospective streamflow data for the Missouri River
at Omaha for June 2011.
```

Claude will likely write a `boto3` script from scratch, guess at the
bucket layout, and fail if AWS credentials aren't configured.

### Part B — With CLI guidance

Clear context with `/clear`, then try:

```
I want to download NWM retrospective streamflow data for June 2011.
The archive is at s3://noaa-nwm-retro-v2-zarr-pds/

1. Run `aws s3 ls --help` to learn the available flags
2. Explore the bucket to understand the folder structure
3. Identify which prefix holds the streamflow files
4. Run aws s3 sync with --dryrun first so I can see the file count
   and total size before committing to the download
5. Show me the final command to run for real
```

---

## What to notice

- Claude reads `--help` output and navigates the bucket on its own — you don't need to know the layout in advance
- `--dryrun` lets you see exactly what would be downloaded before any data moves
- No boto3, no custom code — just the CLI that's already on your machine
