<?php include 'db.php'; ?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tech Shop</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Tech Shop</h1>
        
        <div class="search-box">
            <form method="GET">
                <label>Check Product Availability (ID):</label>
                <input type="text" name="id" placeholder="Enter product ID" value="<?php echo isset($_GET['id']) ? htmlspecialchars($_GET['id']) : '1'; ?>">
                <button type="submit">Check</button>
            </form>
        </div>

        <div class="results">
            <?php
            if (isset($_GET['id']) && $_GET['id'] !== '') {
                $id = $_GET['id'];
                
                
                $sql = "SELECT name, description, price FROM products WHERE id = $id";
                
                $result = $conn->query($sql);
                
                if (!$result) {
                    
                    echo "<p class='error'>SQL Error: " . htmlspecialchars($conn->error) . "</p>";
                } else {
                    if ($result->num_rows > 0) {
                        while($row = $result->fetch_assoc()) {
                            echo "<div class='product'>";
                            echo "<h3>" . htmlspecialchars($row['name']) . "</h3>";
                            echo "<p>" . htmlspecialchars($row['description']) . "</p>";
                            echo "<p class='price'>$" . htmlspecialchars($row['price']) . "</p>";
                            echo "</div>";
                        }
                    } else {
                        echo "<p class='info'>No product found with that ID.</p>";
                    }
                }
            }
            ?>
        </div>
        
    </div>
</body>
</html>
