param(
  [string]$AppUrl = "http://localhost:3000"
)

$ErrorActionPreference = "Stop"
$stripeCmd = Join-Path $env:APPDATA "npm\stripe.cmd"
$projectRoot = Split-Path $PSScriptRoot -Parent
$envPath = Join-Path $projectRoot ".env.local"

if (-not (Test-Path $stripeCmd)) {
  throw "Stripe CLI not found. Run npm run setup:stripe first."
}

Write-Host ""
Write-Host "Forwarding Stripe webhooks to $AppUrl/api/stripe/webhook"
Write-Host "Copy the whsec_... secret below into .env.local as STRIPE_WEBHOOK_SECRET"
Write-Host "Press Ctrl+C to stop."
Write-Host ""

& $stripeCmd listen --forward-to "$AppUrl/api/stripe/webhook" --print-secret
