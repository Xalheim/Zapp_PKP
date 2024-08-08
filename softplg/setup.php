<?php

/**
 * -------------------------------------------------------------------------
 * softplg plugin for GLPI
 * Copyright (C) 2024 by the softplg Development Team.
 * -------------------------------------------------------------------------
 *
 * MIT License
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 * --------------------------------------------------------------------------
 */

// wersja pluginu - plugin version
define('PLUGIN_SOFTPLG_VERSION', '0.0.4');

// Minimal GLPI version, inclusive
define("PLUGIN_SOFTPLG_MIN_GLPI_VERSION", "10.0.0");
// Maximum GLPI version, exclusive
define("PLUGIN_SOFTPLG_MAX_GLPI_VERSION", "10.0.99");

// Min. PHP version excl.
define("PLUGIN_SOFTPLG_MIN_PHP_VERSION", "8.0");
/**
 * Init hooks of the plugin.
 * REQUIRED
 *
 * @return void
 */

// funkcja do inicjalizacji wtyczki
function plugin_init_softplg()
{
    global $PLUGIN_HOOKS, $CFG_GLPI;

    $PLUGIN_HOOKS['csrf_compliant']['softplg'] = true;

    // config page - strona konfiguracyjna (pojawia sie ikonka klucza)
    if(Session::haveRight('config', UPDATE))
    {
	$PLUGIN_HOOKS['config_page']['softplg'] = 'front/config.php';
    }

    // rejestracja klasy "Softplg"
    Plugin::registerClass(Softplg::class);
    $PLUGIN_HOOKS['menu_toadd']['softplg'] = ['plugins' => Softplg::class,
					      'tools'   => Softplg::class];

//    $PLUGIN_HOOKS['menu_toadd']['softplg'] = ['plugins' => 'front/softplg.php'];

/*
    if (isset($_SESSION["glpi_plugin_softplg_profile']))
    {
	$PLUGIN_HOOKS['menu_toadd']['softplg'] = [
	    'plugins' => Example::class,
            'tools' => Example::class
	];

        $PLUGIN_HOOKS[Hooks::HELPDESK_MENU_ENTRY]['softplg'] = true;
        $PLUGIN_HOOKS[Hooks::HELPDESK_MENU_ENTRY_ICON]['softplg'] = 'fas fa-cogs';

  }*/

}
/**
 * Get the name and the version of the plugin
 * REQUIRED
 *
 * @return array
 */

function plugin_version_softplg()
{
    return [
        'name'           => 'softplg',
        'version'        =>  PLUGIN_SOFTPLG_VERSION,
        'author'         => 'KingaM',
        'license'        => 'GPLv3',
        'homepage'       => '<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUJcmljayByb2xs">link</a>',
        'requirements'   => [
            'glpi' => [
                'min' => PLUGIN_SOFTPLG_MIN_GLPI_VERSION,
                'max' => PLUGIN_SOFTPLG_MAX_GLPI_VERSION,
            ],
	    'php' => [
		'min' => PLUGIN_SOFTPLG_MIN_PHP_VERSION
	    ]
        ]
    ];
}

/**
 * Check pre-requisites before install
 * OPTIONNAL, but recommanded
 *
 * @return boolean
 */
function plugin_softplg_check_prerequisites()
{
    return true;
}

/**
 * Check configuration process
 *
 * @param boolean $verbose Whether to display message on failure. Defaults to false
 *
 * @return boolean
 */
function plugin_softplg_check_config($verbose = false)
{
    if (true) { // Your configuration check
        return true;
    }

    if ($verbose) {
        echo __('Installed / not configured', 'softplg');
    }
    return false;
}

function plugin_softplg_options() {
   return [ Plugin::OPTION_AUTOINSTALL_DISABLED => true, ];
}
