# OCR every PNG in a folder with the Windows built-in OCR engine (Windows.Media.Ocr).
# Writes <name>.json next to each image: [{text, x, y, w, h}] per line (pixel coordinates).
# Used by extract_nta_paper.py for NTA papers saved with "Print to PDF" (no text layer).
param([Parameter(Mandatory)][string]$Folder)

Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime]

$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($op, [Type]$t) {
    $task = $asTask.MakeGenericMethod($t).Invoke($null, @($op))
    $task.Wait() | Out-Null
    $task.Result
}

$null = [Windows.Globalization.Language, Windows.Globalization, ContentType = WindowsRuntime]
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new('en-US'))
if (-not $engine) { $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages() }
if (-not $engine) { throw 'No OCR language available' }

Get-ChildItem -Path $Folder -Filter *.png | ForEach-Object {
    $file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($_.FullName)) ([Windows.Storage.StorageFile])
    $stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    $result = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
    $lines = foreach ($l in $result.Lines) {
        $xs = $l.Words | ForEach-Object { $_.BoundingRect }
        $x0 = ($xs | Measure-Object X -Minimum).Minimum
        $y0 = ($xs | Measure-Object Y -Minimum).Minimum
        $x1 = ($xs | ForEach-Object { $_.X + $_.Width } | Measure-Object -Maximum).Maximum
        $y1 = ($xs | ForEach-Object { $_.Y + $_.Height } | Measure-Object -Maximum).Maximum
        [pscustomobject]@{ text = $l.Text; x = $x0; y = $y0; w = $x1 - $x0; h = $y1 - $y0 }
    }
    $stream.Dispose()
    ConvertTo-Json -InputObject @($lines) -Depth 3 | Out-File -Encoding utf8 ($_.FullName -replace '\.png$', '.json')
}
