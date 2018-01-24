<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="8.2.0">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="yes" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="10" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="26" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="con-molex" urn="urn:adsk.eagle:library:165">
<description>&lt;b&gt;Molex Connectors&lt;/b&gt;&lt;p&gt;
&lt;author&gt;Created by librarian@cadsoft.de&lt;/author&gt;</description>
<packages>
<package name="22-23-2021" library_version="1">
<description>.100" (2.54mm) Center Headers - 2 Pin</description>
<wire x1="-2.54" y1="3.175" x2="2.54" y2="3.175" width="0.254" layer="21"/>
<wire x1="2.54" y1="3.175" x2="2.54" y2="1.27" width="0.254" layer="21"/>
<wire x1="2.54" y1="1.27" x2="2.54" y2="-3.175" width="0.254" layer="21"/>
<wire x1="2.54" y1="-3.175" x2="-2.54" y2="-3.175" width="0.254" layer="21"/>
<wire x1="-2.54" y1="-3.175" x2="-2.54" y2="1.27" width="0.254" layer="21"/>
<wire x1="-2.54" y1="1.27" x2="-2.54" y2="3.175" width="0.254" layer="21"/>
<wire x1="-2.54" y1="1.27" x2="2.54" y2="1.27" width="0.254" layer="21"/>
<pad name="1" x="-1.27" y="0" drill="1" shape="long" rot="R90"/>
<pad name="2" x="1.27" y="0" drill="1" shape="long" rot="R90"/>
<text x="-2.54" y="3.81" size="1.016" layer="25" ratio="10">&gt;NAME</text>
<text x="-2.54" y="-5.08" size="1.016" layer="27" ratio="10">&gt;VALUE</text>
</package>
</packages>
<symbols>
<symbol name="MV" library_version="1">
<wire x1="1.27" y1="0" x2="0" y2="0" width="0.6096" layer="94"/>
<text x="2.54" y="-0.762" size="1.524" layer="95">&gt;NAME</text>
<text x="-0.762" y="1.397" size="1.778" layer="96">&gt;VALUE</text>
<pin name="S" x="-2.54" y="0" visible="off" length="short" direction="pas"/>
</symbol>
<symbol name="M" library_version="1">
<wire x1="1.27" y1="0" x2="0" y2="0" width="0.6096" layer="94"/>
<text x="2.54" y="-0.762" size="1.524" layer="95">&gt;NAME</text>
<pin name="S" x="-2.54" y="0" visible="off" length="short" direction="pas"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="22-23-2021" prefix="X" library_version="1">
<description>.100" (2.54mm) Center Header - 2 Pin</description>
<gates>
<gate name="-1" symbol="MV" x="0" y="0" addlevel="always" swaplevel="1"/>
<gate name="-2" symbol="M" x="0" y="-2.54" addlevel="always" swaplevel="1"/>
</gates>
<devices>
<device name="" package="22-23-2021">
<connects>
<connect gate="-1" pin="S" pad="1"/>
<connect gate="-2" pin="S" pad="2"/>
</connects>
<technologies>
<technology name="">
<attribute name="MF" value="MOLEX" constant="no"/>
<attribute name="MPN" value="22-23-2021" constant="no"/>
<attribute name="OC_FARNELL" value="1462926" constant="no"/>
<attribute name="OC_NEWARK" value="25C3832" constant="no"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="5V" library="con-molex" library_urn="urn:adsk.eagle:library:165" deviceset="22-23-2021" device=""/>
<part name="12V" library="con-molex" library_urn="urn:adsk.eagle:library:165" deviceset="22-23-2021" device=""/>
<part name="SUITCASE5" library="con-molex" library_urn="urn:adsk.eagle:library:165" deviceset="22-23-2021" device=""/>
<part name="LID" library="con-molex" library_urn="urn:adsk.eagle:library:165" deviceset="22-23-2021" device=""/>
<part name="LIGHTS5" library="con-molex" library_urn="urn:adsk.eagle:library:165" deviceset="22-23-2021" device=""/>
<part name="BOX" library="con-molex" library_urn="urn:adsk.eagle:library:165" deviceset="22-23-2021" device=""/>
<part name="LIGHTS12" library="con-molex" library_urn="urn:adsk.eagle:library:165" deviceset="22-23-2021" device=""/>
<part name="SUITCASE12" library="con-molex" library_urn="urn:adsk.eagle:library:165" deviceset="22-23-2021" device=""/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="5V" gate="-1" x="27.94" y="27.94" rot="R270"/>
<instance part="5V" gate="-2" x="25.4" y="27.94" rot="R270"/>
<instance part="12V" gate="-1" x="68.58" y="27.94" rot="R270"/>
<instance part="12V" gate="-2" x="66.04" y="27.94" rot="R270"/>
<instance part="SUITCASE5" gate="-1" x="5.08" y="48.26" rot="R90"/>
<instance part="SUITCASE5" gate="-2" x="7.62" y="48.26" rot="R90"/>
<instance part="LID" gate="-1" x="20.32" y="48.26" rot="R90"/>
<instance part="LID" gate="-2" x="22.86" y="48.26" rot="R90"/>
<instance part="LIGHTS5" gate="-1" x="35.56" y="48.26" rot="R90"/>
<instance part="LIGHTS5" gate="-2" x="38.1" y="48.26" rot="R90"/>
<instance part="BOX" gate="-1" x="48.26" y="48.26" rot="R90"/>
<instance part="BOX" gate="-2" x="50.8" y="48.26" rot="R90"/>
<instance part="LIGHTS12" gate="-1" x="60.96" y="48.26" rot="R90"/>
<instance part="LIGHTS12" gate="-2" x="63.5" y="48.26" rot="R90"/>
<instance part="SUITCASE12" gate="-1" x="73.66" y="48.26" rot="R90"/>
<instance part="SUITCASE12" gate="-2" x="76.2" y="48.26" rot="R90"/>
</instances>
<busses>
</busses>
<nets>
<net name="VDD" class="0">
<segment>
<pinref part="5V" gate="-2" pin="S"/>
<wire x1="25.4" y1="30.48" x2="25.4" y2="35.56" width="0.1524" layer="91"/>
<wire x1="25.4" y1="35.56" x2="20.32" y2="35.56" width="0.1524" layer="91"/>
<pinref part="SUITCASE5" gate="-1" pin="S"/>
<wire x1="20.32" y1="35.56" x2="5.08" y2="35.56" width="0.1524" layer="91"/>
<wire x1="5.08" y1="35.56" x2="5.08" y2="45.72" width="0.1524" layer="91"/>
<wire x1="25.4" y1="35.56" x2="35.56" y2="35.56" width="0.1524" layer="91"/>
<junction x="25.4" y="35.56"/>
<pinref part="BOX" gate="-1" pin="S"/>
<wire x1="35.56" y1="35.56" x2="48.26" y2="35.56" width="0.1524" layer="91"/>
<wire x1="48.26" y1="35.56" x2="48.26" y2="45.72" width="0.1524" layer="91"/>
<pinref part="LID" gate="-1" pin="S"/>
<wire x1="20.32" y1="45.72" x2="20.32" y2="35.56" width="0.1524" layer="91"/>
<junction x="20.32" y="35.56"/>
<pinref part="LIGHTS5" gate="-1" pin="S"/>
<wire x1="35.56" y1="45.72" x2="35.56" y2="35.56" width="0.1524" layer="91"/>
<junction x="35.56" y="35.56"/>
<label x="5.08" y="40.64" size="1.778" layer="95" rot="R90"/>
<label x="20.32" y="40.64" size="1.778" layer="95" rot="R90"/>
<label x="35.56" y="40.64" size="1.778" layer="95" rot="R90"/>
<label x="48.26" y="40.64" size="1.778" layer="95" rot="R90"/>
</segment>
<segment>
<pinref part="12V" gate="-2" pin="S"/>
<wire x1="66.04" y1="30.48" x2="66.04" y2="35.56" width="0.1524" layer="91"/>
<pinref part="LIGHTS12" gate="-1" pin="S"/>
<wire x1="66.04" y1="35.56" x2="60.96" y2="35.56" width="0.1524" layer="91"/>
<wire x1="60.96" y1="35.56" x2="60.96" y2="45.72" width="0.1524" layer="91"/>
<wire x1="66.04" y1="35.56" x2="73.66" y2="35.56" width="0.1524" layer="91"/>
<junction x="66.04" y="35.56"/>
<pinref part="SUITCASE12" gate="-1" pin="S"/>
<wire x1="73.66" y1="35.56" x2="73.66" y2="45.72" width="0.1524" layer="91"/>
<label x="60.96" y="40.64" size="1.778" layer="95" rot="R90"/>
<label x="73.66" y="40.64" size="1.778" layer="95" rot="R90"/>
<label x="76.2" y="40.64" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
<net name="GND" class="0">
<segment>
<pinref part="5V" gate="-1" pin="S"/>
<wire x1="27.94" y1="30.48" x2="27.94" y2="33.02" width="0.1524" layer="91"/>
<wire x1="27.94" y1="33.02" x2="38.1" y2="33.02" width="0.1524" layer="91"/>
<pinref part="BOX" gate="-2" pin="S"/>
<wire x1="38.1" y1="33.02" x2="50.8" y2="33.02" width="0.1524" layer="91"/>
<wire x1="50.8" y1="33.02" x2="50.8" y2="45.72" width="0.1524" layer="91"/>
<wire x1="27.94" y1="33.02" x2="22.86" y2="33.02" width="0.1524" layer="91"/>
<junction x="27.94" y="33.02"/>
<pinref part="SUITCASE5" gate="-2" pin="S"/>
<wire x1="22.86" y1="33.02" x2="7.62" y2="33.02" width="0.1524" layer="91"/>
<wire x1="7.62" y1="33.02" x2="7.62" y2="45.72" width="0.1524" layer="91"/>
<pinref part="LIGHTS5" gate="-2" pin="S"/>
<wire x1="38.1" y1="45.72" x2="38.1" y2="33.02" width="0.1524" layer="91"/>
<junction x="38.1" y="33.02"/>
<pinref part="LID" gate="-2" pin="S"/>
<wire x1="22.86" y1="45.72" x2="22.86" y2="33.02" width="0.1524" layer="91"/>
<junction x="22.86" y="33.02"/>
<label x="7.62" y="40.64" size="1.778" layer="95" rot="R90"/>
<label x="22.86" y="40.64" size="1.778" layer="95" rot="R90"/>
<label x="38.1" y="40.64" size="1.778" layer="95" rot="R90"/>
<label x="50.8" y="40.64" size="1.778" layer="95" rot="R90"/>
</segment>
<segment>
<pinref part="12V" gate="-1" pin="S"/>
<wire x1="68.58" y1="30.48" x2="68.58" y2="33.02" width="0.1524" layer="91"/>
<wire x1="68.58" y1="33.02" x2="63.5" y2="33.02" width="0.1524" layer="91"/>
<pinref part="LIGHTS12" gate="-2" pin="S"/>
<wire x1="63.5" y1="33.02" x2="63.5" y2="45.72" width="0.1524" layer="91"/>
<wire x1="68.58" y1="33.02" x2="76.2" y2="33.02" width="0.1524" layer="91"/>
<junction x="68.58" y="33.02"/>
<pinref part="SUITCASE12" gate="-2" pin="S"/>
<wire x1="76.2" y1="33.02" x2="76.2" y2="45.72" width="0.1524" layer="91"/>
<label x="63.5" y="40.64" size="1.778" layer="95" rot="R90"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
<compatibility>
<note version="8.2" severity="warning">
Since Version 8.2, Eagle supports online libraries. The ids
of those online libraries will not be understood (or retained)
with this version.
</note>
</compatibility>
</eagle>
