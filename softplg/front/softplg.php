<?php
use GlpiPlugin\Softplg\Softplg;
include ('../../../inc/includes.php');

Html::header("LIST");

Search::show(Softplg::class);

Html::footer();
