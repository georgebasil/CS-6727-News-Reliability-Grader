<?php
	$siteToAnalyze = "empty";
	
	$_POST = json_decode(file_get_contents('php://input'), true);
	if(isset($_POST["siteToAnalyze"])) {
		$siteToAnalyze = $_POST["siteToAnalyze"];
	}
	
	$command = escapeshellcmd('<PATH-TO-CGI-BIN-DIRECTORY>\classify.py "' .$siteToAnalyze. '"');
	$output = shell_exec($command);
	
	$output_json = json_decode($output);
	
	$myObj = new stdClass();
	$myObj->score = $output_json->{'score'};
	$myObj->trustedRegistrar = $output_json->{'trustedRegistrar'};
	$myObj->trustedDomainAge = $output_json->{'trustedDomainAge'};
	$myObj->trustedTLD = $output_json->{'trustedTLD'};

	$myJSON = json_encode($myObj);

	echo $myJSON;
?>
