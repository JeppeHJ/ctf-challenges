<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

$ingredient = $_GET['ingredient'] ?? '';

$denyListCharacters = ['&', '|', '`', '>', '<', '(', ')', '[', ']', '\\', '"', '*', '/', ' '];
$denyListCommands = ['rm', 'mv', 'cp', 'cat', 'echo', 'touch', 'chmod', 'chown', 'kill', 'ps', 'top', 'find'];

function loadSecretRecipe() {
    file_get_contents('/flag.txt');
}

function sanitizeCharacters($input) {
    for ($i = 0; $i < strlen($input); $i++) {
        if (in_array($input[$i], $GLOBALS['denyListCharacters'], true)) {
            return 'Illegal character detected!';
        }
    }
    return $input;
}

function sanitizeCommands($input) {
    foreach ($GLOBALS['denyListCommands'] as $cmd) {
        if (stripos($input, $cmd) !== false) {
            return 'Illegal command detected!';
        }
    }
    return $input;
}

function analyze($ingredient) {
    $tmp = sanitizeCharacters($ingredient);
    if ($tmp !== $ingredient) {
        return $tmp;
    }

    $tmp = sanitizeCommands($ingredient);
    if ($tmp !== $ingredient) {
        return $tmp;
    }

    return shell_exec("bash -c './quality.sh $ingredient' 2>&1");
}

$result = $ingredient !== '' ? analyze($ingredient) : '';
?>
<!doctype html>
<meta charset="utf-8">
<title>Baking Bad purity tester</title>
<link rel="stylesheet" href="static/css/style.css">
<img src="static/images/background.png" alt="Brunnerne lab prepping cookies" class="hero">

<h1>Brunnerne Baking Simulator</h1>
<p class="lead">
  We need to bake. A higher purity in the dough means a higher yield.
  A higher purity means customers pay more. Insert any ingredient and the simulator will analyze and return the resulting purity.
</p>

<form>
  <input name="ingredient" placeholder="chocolate"
         value="<?=htmlspecialchars($ingredient)?>">
  <button>Analyze</button>
</form>

<?php if($result!==''): ?>
  <pre><?= $result ?></pre>
<?php endif; ?>
