# Vitruvius — Local Dev Database Setup (Windows)
# Sprint KG Phase 0 (Readiness)
#
# Usage:
#   .\scripts\vitruvius\db\dev_setup.ps1
#
# Prerequisites: Docker Desktop installed and running.

param(
    [switch]$Stop,
    [switch]$Reset,
    [switch]$Status
)

$composeFile = "$PSScriptRoot\..\..\..\docker-compose.yml"

function Test-DockerRunning {
    try {
        $null = docker info 2>$null
        return $?
    } catch {
        return $false
    }
}

if ($Status) {
    Write-Host "Checking service status..." -ForegroundColor Cyan
    docker compose -f $composeFile ps
    exit 0
}

if ($Stop) {
    Write-Host "Stopping Vitruvius dev services..." -ForegroundColor Yellow
    docker compose -f $composeFile down
    Write-Host "Services stopped." -ForegroundColor Green
    exit 0
}

if ($Reset) {
    Write-Host "Resetting Vitruvius dev services (data will be lost)..." -ForegroundColor Red
    docker compose -f $composeFile down -v
    Write-Host "Volumes removed. Starting fresh..." -ForegroundColor Yellow
    docker compose -f $composeFile up -d
    Write-Host "Services restarted with fresh volumes." -ForegroundColor Green
    exit 0
}

if (-not (Test-DockerRunning)) {
    Write-Error "Docker is not running. Please start Docker Desktop first."
    exit 1
}

Write-Host "Starting Vitruvius dev services (Neo4j + PostgreSQL)..." -ForegroundColor Cyan
docker compose -f $composeFile up -d

if (-not $?) {
    Write-Error "Failed to start services. Check Docker logs."
    exit 1
}

Write-Host "Waiting for services to be healthy..." -ForegroundColor Cyan
$maxWait = 60
$elapsed = 0
while ($elapsed -lt $maxWait) {
    Start-Sleep -Seconds 2
    $elapsed += 2
    $neo4j = docker compose -f $composeFile ps neo4j --format "{{.Health}}" 2>$null
    $postgres = docker compose -f $composeFile ps postgres --format "{{.Health}}" 2>$null
    if ($neo4j -eq "healthy" -and $postgres -eq "healthy") {
        break
    }
}

Write-Host "`n=== Vitruvius Dev Services ===" -ForegroundColor Green
Write-Host "Neo4j Browser:   http://localhost:7474"
Write-Host "Neo4j Bolt:      bolt://localhost:7687"
Write-Host "Neo4j Auth:      neo4j / vitruvius"
Write-Host "PostgreSQL:      localhost:5432"
Write-Host "PostgreSQL Auth: vitruvius / vitruvius"
Write-Host "`nTo stop:  .\scripts\vitruvius\db\dev_setup.ps1 -Stop"
Write-Host "To reset: .\scripts\vitruvius\db\dev_setup.ps1 -Reset"
