<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
    encoding="utf-8" indent="yes" media-type="text/html" method="xml"
    omit-xml-declaration="yes" />
  <xsl:param name="google_api_key" />
  <xsl:template match="/event">
    <html lang="en" xml:lang="en">
      <head>
        <title>
          <xsl:value-of select="origin/time/value" />
        </title>
        <link href="http://www.seishub.org/css/components.css" rel="stylesheet"
          type="text/css" />
        <script type="text/javascript">
          <xsl:attribute name="src">
            <xsl:text>http://www.google.com/jsapi?key=</xsl:text>
            <xsl:value-of select="$google_api_key" />
          </xsl:attribute>
        </script>
        <script type="text/javascript">
                    <xsl:text>
<![CDATA[
    google.load("maps", "2.x");
    
    function initialize() {
      if (GBrowserIsCompatible()) {
        var map = new GMap2(document.getElementById("map_canvas"));
]]>
                    </xsl:text>
                    <xsl:text>var lat = </xsl:text>
          <xsl:value-of select="origin/latitude/value" />
                    <xsl:text>; var long = </xsl:text>
          <xsl:value-of select="origin/longitude/value" />
                    <xsl:text>;</xsl:text>
                    <xsl:text>
<![CDATA[
        map.addControl(new GLargeMapControl());
        map.addControl(new GMapTypeControl());
        map.addMapType(G_PHYSICAL_MAP);
        var center = new GLatLng(lat, long);
        map.setCenter(center, 7);
        var marker = new GMarker(center, {});
        map.addOverlay(marker);
      }
    }
]]>
                    </xsl:text>
                </script>
      </head>
      <body onload="initialize()" onunload="GUnload()">
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
