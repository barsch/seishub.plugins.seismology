// SeisGram2K version 2, SeisGram2K/LiveSeis N-comp script, A.Lomax 26JUL2000
// 26JUL2000 AJL ver _02 - event parameters added
// 19AUG2000 AJL ver _03 - JDK1.0 removed, support for additional program arguments added
// 19JAN2005 AJL ver _04 - JDK1.1 check removed
// 26FEB2009 AJL ver _04 - check that navigatior supports Java removed

// NOTE: lines that may need to be changed during installation
// are indicated by "// !!CHANGE HERE" ... // !!END CHANGE HERE


// declare SeisGram2K parameters object
function SeisGram2KParams(java_version, mode, locale, wild_chars) {
	this.java_version = java_version;
	this.set_java_version = set_java_version
	this.mode = mode;
	this.set_mode = set_mode
	this.locale = locale;
	this.set_locale = set_locale;
	this.wild_chars = wild_chars;
	this.set_wild_chars = set_wild_chars;
	this.replaceWildChars = replaceWildChars;
}
function set_java_version(java_version) {
	this.java_version = java_version;
}
function set_mode(mode) {
	this.mode = mode;
}
function set_locale(locale) {
	this.locale = locale;
}
function set_wild_chars(wild_chars) {
	this.wild_chars = wild_chars;
}
function replaceWildChars(name, nwild) {
	var newString = "";
	var replaceChrs = "";
	var n, ndx = 0;
	if (this.wild_chars.length < 1)
		return(null);
	for (n = 0; n < nwild; n++) {
		ndx = this.wild_chars.indexOf(":", ndx);
		if (ndx < 0)
			return(null);
		ndx++;
	}
	replaceChrs = this.wild_chars.substring(ndx, ndx + 1);
	ndx = name.indexOf("*", 0);
	if (ndx < 0)
		return(null);
	newString = name.substring(0, ndx) + replaceChrs + name.substring(ndx + 1, name.length);
	return(newString);
}



// !!CHANGE HERE
// default values of applet parameters:
//var seisGram2KParams = new SeisGram2KParams("AUTO", "STANDARD", "en_US", "Z:N:E");
var seisGram2KParams = new SeisGram2KParams("JDK11", "STANDARD", "en_US", "Z:N:E");
// sismo des ecoles:
//var seisGram2KParams = new SeisGram2KParams("JDK11", "STANDARD", "fr_FR", "Z:N:E", "Z:N:E");
// !!END CHANGE HERE



//  function to launch SeisGram2K in LiveSeis mode with N channels

function seis_view_n(windowName, titleString, liveseis, seischannel, locale, mode,
	channelformat, binarytype, pickformat, pickfile, addlArguments) {

/* Arguments:

   windowName    - arbitrary name for browser window conaining SeisGram2K
   titleString   - String to be displayed in title bar of browser window
   liveseis      - String with '#' separator contianing: total number of segments, number of segments to display, update time interval in seconds, minimum peak amplitude of initial display amplitude (optional, allows supression of display of background noise at large amplitude.
   seischannel   - array of Strings giving relative path and filename template for each channel.  Filename template must contain a set of '%' or '&' characters as place holders for the segment index in the filnemae.  Thus for filenames ./data/seg000.sac, ./data/seg001.sac, etc, the template would be './data/seg%%%.sac' or './data/seg&&&.sac'.  NOTE! - The last channel template in the list must be also be the channel that has the last updated "liveseis.last" index file, this index file is used to control the updating of all the channels in the array.
   locale        - language locale String (see SeisGram2K help)
   mode          - SeisGram2K mode String (see SeisGram2K help)
   channelformat - channel format String  (see SeisGram2K help)
   binarytype    - binary type String  (see SeisGram2K help)
   pickformat    - pick file format String  (see SeisGram2K help)
   pickfile      - pick file name String  (see SeisGram2K help)
   addlArguments     - additional SeisGram2K program arguments  (see SeisGram2K help)
		array of parameter/value String pairs

   Example (SeisGram2K):
      javascript:seis_view_n('seisview', '1999.12.22-17.37', null,
		['./lomax/1999_data/19991222/1999.12.22-17.37.01.CIV.LH-Z.SAC',
		 './lomax/1999_data/19991222/1999.12.22-17.37.04.MNTF.LH-Z.SAC',
		 './lomax/1999_data/19991222/1999.12.22-17.37.04.SETF.LH-Z.SAC'],
		 null, null, 'SAC_BINARY', 'PC_INTEL', 'SAC_STD_OFFSET', ' ',
		 [['event.id', 1234],
		 ['event.info', '22 December 1999\\nM=4.7 Vintimiglia\\n(France-Italy Border)'],
		 ['event.url', 'http://hostname/cgi-bin/getpicks'],
		 ['event.protocol', 'NON_LIN_LOC_XML'])

   Example (LiveSeis):
      javascript:seis_view_n('liveseis_tgrs',
		'LiveSeis: ReNaSS-NICE - TOUF/AUTN/REVF - SP - SH',
		'60#5#60.0#1500.0', ['./data/NICE/TOUF/SH/sac/NICE%%%.TOUF.Z.sac.gz',
		'./data/NICE/AUTN/SH/sac/NICE%%%.AUTN.Z.sac.gz',
		'./data/NICE/REVF/SH/sac/NICE%%%.REVF.Z.sac.gz'],
		null, null, 'SAC_BINARY', 'SUN_UNIX', 'NON_LIN_LOC',
		' ', [['liveseis.contig', 'YES']])

*/


	// display browser
	//alert("Your browser is:" + navigator.appName + " | " + navigator.appVersion);


	// check that navigatior supports Java
	//if (!navigator.javaEnabled()) {
	//	alert("WARNING - Java is not enabled on your browser!");
	//}

 	// check that at least one channel is selected
	if (seischannel[0] == null) {
		alert("SeisGram2K: Error - must specify at least one channel file!");
		return;
	}

 	// expand any wildcard characters in seischannel[0]
	var ndx = -1;
	if (seischannel.length <= 3 && (ndx = seischannel[0].indexOf("*", 0)) >= 0) {
		seischannel[2] = seisGram2KParams.replaceWildChars(seischannel[0], 2);
		seischannel[1] = seisGram2KParams.replaceWildChars(seischannel[0], 1);
		seischannel[0] = seisGram2KParams.replaceWildChars(seischannel[0], 0);
	}


	// open new window for HTML and applet
// !!CHANGE HERE
	var applet_frame_number = 1;	// use -1 to disable frame mode
// !!END CHANGE HERE
	var viewer_doc = null;
		// use frames, puts applet in frame
		// check if not in frames
		if (applet_frame_number < 0 || parent.frames[applet_frame_number] == null) {
			nwin = window.open("", "seisView"+windowName, "menubar=yes,toolbar=no,scrollbars=no,resizable=yes,status=no,width=400,height=100");
			viewer_doc = nwin.document;
		} else {
			viewer_doc = parent.frames[applet_frame_number].document;
		}
		// write html for new applet
		viewer_doc.open();
		// destroy any existing applet
// !!CHANGE HERE
// !! UNCOMMENT FOLLOWING TO DESTROY EXISTING APPLETS WHEN NEW APPLET LAUNCHED
// !! RECOMMENDED NOT TO DESTROY EXISTING APPLETS IN LIVE-SEIS MODE
/*
		var napplets = viewer_doc.applets.length;
		if (napplets > 0) {
			var n;
			for (n = 0; n < napplets; n++)
				viewer_doc.applets[n].destroy();
		}
		viewer_doc.writeln("<! destroyed " + napplets + " old applets>");
*/
// !!END CHANGE HERE
	    viewer_doc.writeln("<HTML>");
	    viewer_doc.writeln("<HEAD>");
	    viewer_doc.writeln("<TITLE>SeisGram2K</TITLE>");
	    viewer_doc.writeln("</HEAD>");
		// applet tag
// !!CHANGE HERE
		viewer_doc.writeln(
		"<APPLET archive=./java/SeisGram2K53.jar code=net.alomax.seisgram2k.SeisGram2KApp.class width=100% height=100%>");
// !!END CHANGE HERE

	// applet parameters
	if (titleString != null)
        	viewer_doc.writeln("<param name=title value='"+titleString+"'>");
	if (locale == null)
		locale = seisGram2KParams.locale;
        viewer_doc.writeln("<param name=locale value='"+locale+"'>");
	if (mode == null)
		mode =  seisGram2KParams.mode;
        viewer_doc.writeln("<param name=mode value='"+mode+"'>");
	if (pickformat == null)
		pickformat = "NON_LIN_LOC";
        viewer_doc.writeln(
		"<param name=pickformat value='"+pickformat+"'>");
        //viewer_doc.writeln("<param name=pickfile value='"+pickfile+"'>");
	if (channelformat == null)
		channelformat = "SAC_BINARY";
        viewer_doc.writeln(
		"<param name=channelformat value='"+channelformat+"'>");
	if (binarytype == null)
		binarytype = "PC_INTEL";
        viewer_doc.writeln(
		"<param name=binarytype value='"+binarytype+"'>");
        if (liveseis != null) {
        	viewer_doc.writeln(
			"<param name=liveseis value='"+liveseis+"'>");
		// data channels
		for (n = 0; n < seischannel.length; n++)
	 	       if (seischannel[n] != null)
 	 		      	viewer_doc.writeln(
					"<param name=livechannel"+n+" value='"+seischannel[n]+"'>");
	} else {
		// data channels
		for (n = 0; n < seischannel.length; n++)
	 	       if (seischannel[n] != null)
 	 		      	viewer_doc.writeln(
					"<param name=channel"+n+" value='"+seischannel[n]+"'>");
	}

	// additional program arguments
	if (addlArguments != null) {
		for (n = 0; n < addlArguments.length; n++) {
			if (addlArguments[n] != null
					&& addlArguments[n][0] != null&& addlArguments[n][1] != null)
 				viewer_doc.writeln( "<param name="+addlArguments[n][0] +
					" value='"+addlArguments[n][1]+"'>");
		}
	}

    viewer_doc.writeln("</APPLET>");

	viewer_doc.writeln("<FONT SIZE=-1>Your browser: Name:" + navigator.appName + "  Version:" + navigator.appVersion + "</FONT>");

	// write closing HTML text
    viewer_doc.writeln("</HTML>");

    viewer_doc.close();

};


