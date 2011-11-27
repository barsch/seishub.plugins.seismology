<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
    encoding="utf-8" indent="yes" media-type="text/html" method="xml"
    omit-xml-declaration="yes" />
  <xsl:template match="/event">
    <html lang="en" xml:lang="en">
      <head>
        <title>
          <xsl:value-of select="origin/time/value" />
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
          <xsl:value-of select="origin/latitude/value" />
          <xsl:text>; var long = </xsl:text>
          <xsl:value-of select="origin/longitude/value" />
          <xsl:text>; var title = "</xsl:text>
          <xsl:value-of select="origin/time/value" />
          <xsl:text>";</xsl:text>
          <xsl:text>
<![CDATA[
    var latlng = new google.maps.LatLng(lat, long);
    var myOptions = {
        zoom: 7,
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
          <xsl:value-of select="origin/time/value" />
          <xsl:text> +- </xsl:text>
          <xsl:value-of select="origin/time/uncertainty" />
        </h1>
        <table>
          <tr>
            <th>Magnitude (<xsl:value-of select="magnitude/type" />)</th>
            <td>
              <xsl:value-of select="magnitude/mag/value" />
              <xsl:text> +- </xsl:text>
              <xsl:value-of select="magnitude/mag/uncertainty" />
            </td>
          </tr>
          <tr>
            <th>Latitude</th>
            <td>
              <xsl:value-of select="origin/latitude/value" />
              <xsl:text> +- </xsl:text>
              <xsl:value-of select="origin/latitude/uncertainty" />
            </td>
          </tr>
          <tr>
            <th>Longitude</th>
            <td>
              <xsl:value-of select="origin/longitude/value" />
              <xsl:text> +- </xsl:text>
              <xsl:value-of select="origin/longitude/uncertainty" />
            </td>
          </tr>
          <tr>
            <th>Depth</th>
            <td>
              <xsl:value-of select="origin/depth/value" />
              <xsl:text> +- </xsl:text>
              <xsl:value-of select="origin/depth/uncertainty" />
            </td>
          </tr>
          <xsl:if test="focalMechanism/momentTensor/tensor/Mrr/value!=''">
            <tr>
              <th>Focal Mechanism</th>
              <td>
                <img>
                  <xsl:attribute name="src">
                    <xsl:text>/seismology/event/plotBeachball</xsl:text>
                    <xsl:text>?size=150&amp;linewidth=1&amp;fm=</xsl:text>
                    <xsl:value-of
                      select="focalMechanism/momentTensor/tensor/Mrr/value" />
                    <xsl:text>,</xsl:text>
                    <xsl:value-of
                      select="focalMechanism/momentTensor/tensor/Mtt/value" />
                    <xsl:text>,</xsl:text>
                    <xsl:value-of
                      select="focalMechanism/momentTensor/tensor/Mpp/value" />
                    <xsl:text>,</xsl:text>
                    <xsl:value-of
                      select="focalMechanism/momentTensor/tensor/Mrp/value" />
                    <xsl:text>,</xsl:text>
                    <xsl:value-of
                      select="focalMechanism/momentTensor/tensor/Mrt/value" />
                    <xsl:text>,</xsl:text>
                    <xsl:value-of
                      select="focalMechanism/momentTensor/tensor/Mtp/value" />
                  </xsl:attribute>
                </img>
              </td>
            </tr>
          </xsl:if>
        </table>
        <div id="map_canvas" style="margin-top: 20px; width: 700px; height: 500px" />
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
