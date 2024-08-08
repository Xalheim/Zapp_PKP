<?php

include("../../../inc/includes.php");

Session::checkRight("config", UPDATE);

Plugin::load('softplg');

Html::header("TITLE", $_SERVER['PHP_SELF'], "config", "plugins");

// include("../index.php");

echo __("Hello, this is the plugin config page", 'softplg');

Html::footer("stopka");

?>
