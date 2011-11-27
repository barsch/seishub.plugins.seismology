<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
    encoding="utf-8" indent="yes" media-type="text/html" method="xml"
    omit-xml-declaration="yes" />
  <xsl:template
    match="/xseed/station_control_header/channel_identifier/channel_identifier">
    <xsl:value-of select="current()" />
    <br />
  </xsl:template>
  <xsl:template match="/xseed">
    <html lang="en" xml:lang="en">
      <head>
        <title>
          <xsl:value-of
            select="station_control_header/station_identifier/station_call_letters"
           />
        </title>
        <link href="http://www.seishub.org/css/components.css" rel="stylesheet"
          type="text/css" />
        <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"> </script>
        <script type="text/javascript">
          <xsl:text>
<![CDATA[
  function initialize()
  {
]]>
          </xsl:text>
          <xsl:text>var lat = </xsl:text>
          <xsl:value-of select="station_control_header/station_identifier/latitude" />
          <xsl:text>; var long = </xsl:text>
          <xsl:value-of select="station_control_header/station_identifier/longitude" />
          <xsl:text>; var title = "</xsl:text>
          <xsl:value-of select="station_control_header/station_identifier/station_call_letters" />
          <xsl:text>";</xsl:text>
          <xsl:text>
<![CDATA[
    var latlng = new google.maps.LatLng(lat, long);
    var myOptions = {
        zoom: 13,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    var marker = new google.maps.Marker({
        position: latlng, 
        map: map,
        title: title
    });
  }
]]>
          </xsl:text>
        </script>
      </head>
      <body onload="initialize()">
        <h1>
          <xsl:value-of
            select="station_control_header/station_identifier/station_call_letters"
           />
        </h1>
        <table>
          <tr>
            <th>Station call letters</th>
            <td>
              <xsl:value-of
                select="station_control_header/station_identifier/station_call_letters"
               />
            </td>
          </tr>
          <tr>
            <th>Latitude</th>
            <td>
              <xsl:value-of
                select="station_control_header/station_identifier/latitude" />
            </td>
          </tr>
          <tr>
            <th>Longitude</th>
            <td>
              <xsl:value-of
                select="station_control_header/station_identifier/longitude" />
            </td>
          </tr>
          <tr>
            <th>Elevation</th>
            <td>
              <xsl:value-of
                select="station_control_header/station_identifier/elevation" />
            </td>
          </tr>
          <tr>
            <th>Site name</th>
            <td>
              <xsl:value-of
                select="station_control_header/station_identifier/site_name" />
            </td>
          </tr>
          <tr>
            <th>Channels</th>
            <td>
              <xsl:apply-templates
                select="/xseed/station_control_header/channel_identifier/channel_identifier"
               />
            </td>
          </tr>
        </table>
        <div id="map_canvas"
          style="margin-top: 20px; width: 700px; height: 500px" />
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
