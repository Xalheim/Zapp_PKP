<?php
namespace GlpiPlugin\Softplg;

class Softplg extends CommonDBTM {
   public function showForm($ID, array $options = []) {
    // Get and display records
    $records = $this->getRecords();

    $out = '<table class="tab_cadre_fixe">';
    $out .= '<tr><th>ID</th><th>Name</th></tr>';  // Adjust columns as needed

    if (!empty($records)) {
        foreach ($records as $record) {
            $out .= '<tr>';
            $out .= '<td>' . htmlspecialchars($record['id']) . '</td>';
            $out .= '<td>' . htmlspecialchars($record['name']) . '</td>';  // Adjust fields as needed
            $out .= '</tr>';
        }
    } else {
        $out .= '<tr><td colspan="2">' . __('No records found', 'softplg') . '</td></tr>';
    }

    $out .= '</table>';

    // Output or return the HTML
    if (isset($options['display']) && $options['display'] == true) {
        echo $out;
    } else {
        return $out;
    }
   }

     public function getRecords() {
   	$query = "SELECT * FROM glpi_plugin_softplg_util";
   	$result = $this->db->query($query);

   	$records = [];
   	while ($data = $this->db->fetch_array($result)) {
      	    $records[] = $data;
        }
        return $records;
     }
}
