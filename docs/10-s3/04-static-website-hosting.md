# 04 — S3 Static Website Hosting

## What this covers
Serving a website directly from S3, with no EC2 instance or web server
involved.

## What I did
- Created a dedicated public bucket (cloudlearner-website-vershi1ma),
  separate from the general-purpose lesson bucket, with public access
  intentionally allowed for this specific purpose
- Uploaded a simple index.html
- Enabled static website hosting, set index.html as the index document
- Added a bucket policy granting public s3:GetObject read access
- Verified the site loads live at the S3 website endpoint

## Known limitation (not yet addressed)
Raw S3 static website hosting only serves over HTTP -- there's no way
to get HTTPS on the native S3 website endpoint. The standard real-world
fix is placing CloudFront in front of the bucket to terminate HTTPS
and add CDN caching. This is a legitimate next step, deliberately not
built here to keep this lesson scoped to core S3 hosting mechanics.

## Key takeaway
A large class of real websites (landing pages, docs sites, portfolios)
don't need a server at all -- S3 alone can serve them, cheaply and
without any compute to patch or manage. This bucket is being kept live
as an actual working artifact of the portfolio.
