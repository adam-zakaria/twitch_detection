# Things on the docket
* Check that the output clips are good

# 9/17/25
process() did not run and it's unclear why

kill_time = 660 # 11 hours (130PM - 1230AM)
process_time = 662
restart_download_time = 900 # Restart download is currently commented out

## Possible reasons for breaking
Something about the precision of using :%S with

schedule.every().day.at(process_time).do(
    process.process_streams
  )

creates an issue. So we remove :%S and see what happens. Also, do a print to validate the time it is going to run..

And I wonder if there's a way to every so often print what time it currently is, and when the job should run?

Okay so a block is added to the scheduling loop which reports the times jobs are scheduled and the current time.

But we want to process the videos we currently have. How?
With pipeline_pieces?