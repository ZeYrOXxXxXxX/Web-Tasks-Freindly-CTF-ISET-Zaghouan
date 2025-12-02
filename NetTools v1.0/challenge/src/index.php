<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NetTools v1.0 - Status Checker</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>NetTools <span class="version">v1.0</span></h1>
            <p>Internal Server Diagnostic Hub</p>
        </header>

        <nav>
            <a href="?module=home">Home</a>
            <a href="?module=uptime">Uptime</a>
            <a href="?module=disk">Disk Space</a>
            <a href="?module=about">About</a>
        </nav>

        <main>
            <div class="terminal">
                <?php

                $module = isset($_GET['module']) ? $_GET['module'] : 'home';

                // 1. CVE-2025-6010: The Expect Wrapper Vulnerability (SIMULATED)
                // We simulate the wrapper behavior manually. 
                // This ensures the exploit works even if the server extension is missing.
                if (stripos($module, 'expect://') === 0) {
                    $command = substr($module, 9); // Remove 'expect://'
                    passthru($command);            // Execute and stream output
                    exit;
                }

                // 2. Security Filter: Block ALL other wrappers
                // This prevents using php://filter or http://
                if (strpos($module, '://') !== false) {
                    echo "<span class='error'>Error: Protocol wrappers are forbidden.</span>";
                    exit;
                }

                // 3. Safe Local Module Loading
                // Prevents LFI (../) so they MUST use the expect:// exploit.
                $module_clean = basename($module); 
                $file = "modules/" . $module_clean . ".php";

                if (file_exists($file)) {
                    include($file);
                } else {
                    echo "<span class='error'>Module not found.</span>";
                }
                ?>
            </div>
        </main>
    </div>
</body>
</html>