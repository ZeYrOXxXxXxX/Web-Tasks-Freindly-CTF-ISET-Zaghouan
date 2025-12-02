<?php
$target_dir = "uploads/";
$allowed_exts = ["zip", "tar", "bz2", "7z", "rar"];
$flag_path = "/flag.txt";
$max_file_size = 5 * 1024 * 1024; // 5MB

// --- Helper Functions ---
function displayAlert($message, $type = "info") {
    $icon = match($type) {
        "success" => "✅",
        "danger"  => "🚨",
        "warning" => "⚠️",
        default    => "ℹ️",
    };
    echo "<div class='alert alert-$type d-flex align-items-center gap-2' role='alert'><span class='fs-5'>$icon</span><span>" . htmlspecialchars($message) . "</span></div>";
}

function generateFileName($original_name) {
    $ext = pathinfo($original_name, PATHINFO_EXTENSION);
    $hash = md5(microtime(true) . $original_name);
    return $hash . "." . $ext;
}

// --- Upload Handler ---
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['archiveFile'])) {
    $file = $_FILES['archiveFile'];

    if ($file['error'] !== UPLOAD_ERR_OK) {
        displayAlert("File upload failed with error code: " . (int)$file['error'], "danger");
    } else {
        $file_ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));

        if (!in_array($file_ext, $allowed_exts, true)) {
            displayAlert("Only archives allowed. Rejected type: ." . htmlspecialchars($file_ext), "danger");
        } elseif ($file['size'] > $max_file_size) {
            displayAlert("File too large. Maximum size is 5MB.", "danger");
        } else {
            $new_filename = generateFileName($file['name']);
            $target_file = $target_dir . $new_filename;

            if (move_uploaded_file($file['tmp_name'], $target_file)) {
                displayAlert("File uploaded successfully as: <code>" . htmlspecialchars($new_filename) . "</code>", "success");
            } else {
                displayAlert("Error moving uploaded file.", "danger");
            }
        }
    }
}

// --- View/LFI Handler ---
$file_to_include = $_GET['file'] ?? null;

if ($file_to_include) {
    // 1) Basic Blacklist Filter
    $blacklist = ['php://', 'data://', 'zip://', 'expect://', 'file://', 'glob://', 'phar://', '<?php'];
    $hack_detected = false;
    $low = strtolower($file_to_include);
    foreach ($blacklist as $item) {
        if (str_contains($low, $item)) { $hack_detected = true; break; }
    }

    if ($hack_detected) {
        displayAlert("Hack detected!", "danger");
    } elseif (preg_match('/\.(php|phtml|pht)$/i', $file_to_include)) {
        // 2) Block direct PHP-like extensions
        displayAlert("Access denied! Cannot include .php/.phtml/.pht directly.", "danger");
    } else {
        // 3) The Vulnerability: including user-supplied path
        // open_basedir limits filesystem access; including a ZIP whose comment contains
        // "<?= ... ? >" will still be parsed by PHP and executes.
        echo "<h3 class='h5'>Viewing: <code>" . htmlspecialchars($file_to_include) . "</code></h3><hr class='my-2'>";
        @include($file_to_include);
        echo "<hr class='my-3'>";
        displayAlert("End of archive content view.", "info");
    }
}
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="referrer" content="no-referrer">
  <title>The Archivist's Echo</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
  <nav class="navbar navbar-dark bg-dark mb-4">
    <div class="container">
      <a class="navbar-brand fw-semibold" href="/">💾 The Archivist's Echo</a>
    </div>
  </nav>

  <main class="container" style="max-width: 920px;">
    <div class="row g-4">
      <div class="col-12">
        <div class="alert alert-secondary py-2" role="alert">
          <div class="d-flex flex-wrap align-items-center gap-2">
            <span>Allowed types:</span>
            <code>.zip</code> <code>.tar</code> <code>.bz2</code> <code>.7z</code> <code>.rar</code>
            <span class="ms-2">• Max size: <strong>5 MB</strong></span>
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-6">
        <div class="card shadow-sm h-100">
          <div class="card-header bg-primary text-white">Upload Archive</div>
          <div class="card-body">
            <form action="/" method="POST" enctype="multipart/form-data" class="vstack gap-3">
              <div>
                <label for="archiveFile" class="form-label">Choose an archive</label>
                <input class="form-control" type="file" id="archiveFile" name="archiveFile" accept=".zip,.tar,.bz2,.7z,.rar" required>
              </div>
              <button type="submit" class="btn btn-primary">Upload</button>
            </form>
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-6">
        <div class="card shadow-sm h-100">
          <div class="card-header bg-success text-white">View Archive</div>
          <div class="card-body">
            <p class="mb-2">Enter a file to view it </p>
            <form method="GET" class="mb-2">
              <div class="input-group">
                <span class="input-group-text">File</span>
                <input type="text" class="form-control" name="file" placeholder="name of the file" value="<?= htmlspecialchars($file_to_include ?? '') ?>">
                <button type="submit" class="btn btn-success">View</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <footer class="text-center text-muted mt-5 mb-4 small">
      Challenge by ZeyRoxx
    </footer>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>