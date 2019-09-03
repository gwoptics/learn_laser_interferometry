{%- extends 'basic.tpl' -%}
{% from 'mathjax.tpl' import mathjax %}

<!DOCTYPE html>
<html>
<head>
{%- block header -%}
<meta charset="utf-8" />
<title>{{resources['metadata']['name']}} | Learn Laser Interferometry with Finesse</title>

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>

<style type="text/css">
#gwwrapper {
    margin: 0;
    padding: 0;
}

#gwheader {
    width: 920px;
    margin: 0 auto;
	height: 30px;
}

#gwpage {
    width: 920px;
    background: #FFFFFF;
	margin: 0px auto;
    border: 10px #FFFFFF solid;
}

h1.course-title {
		margin-left: 10px;
		margin-top: -10px;
		margin-bottom: -10px;
    font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
		font-weight: normal;
		font-size: 18px;
}		

#gwmenu {
    font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
    float: left;
    width: 920px;
    height: 52px;
	background: #dbdbdb;
    border: 10px #FFFFFF solid;
    z-index: 9999999;
}

#gwmenu ul {
    margin: 0;
    padding: 6px 0 0 20px;
    list-style: none;
    line-height: normal;
	border: none;
    z-index: 9999999;
}

#gwmenu li {
    float: left;
    text-align: center;
	border: none;
    z-index: 9999999;
}

#gwmenu li:hover {
	background:#bbbbbb;
}

#gwmenu li.last:hover { 
	background:#dbdbdb;
}


#gwmenu ul li
{
  position:relative;
	float:left;
	margin:0;
	padding:0
}

#gwmenu ul ul
{
  font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
	font-size:15px;
	display:none;
	position:absolute;
	top:100%;
	left:0;
	background:#dbdbdb;
	padding:0;
}

#gwmenu ul ul li
{
	float:none;
	width:300px;
	color:#000;
}

#gwmenu ul ul li.sep
{
		border-top: 3px #FFFFFF solid;
}

#gwmenu ul ul a
{
	line-height:120%;
	padding:10px 15px
}

#gwmenu ul ul ul
{
	top:0;
	left:100%
}

#gwmenu ul li:hover > ul
{
	display:block
}

#gwmenu ul a { 
    display: block;
    padding: 0 50px;
    text-decoration: none;
    text-transform: uppercase;
    color: #0F0F0F;
		border: none;
}

#gwmenu ul ul a { 
    text-decoration: none;
    text-transform: none;
		text-align: left;
    color: #0F0F0F;
		border: none;
}

#gwmenu :focus, :active {
		border: 0;
    text-decoration: none;
}

#gwmenu a.last {
    display: block;
    padding: 0px 10px;
    background: none;
    text-decoration: none;
    text-transform: uppercase;
    color: #FFFFFF;
}

#gwmenu .current_page_item a {
    color: #FFFFFF;
}

/** LOGO */

#gwlogo {
    width: 900px;
    height: 130px;
    margin: 0 auto;
}

#gwlogo h2 {
    float: left;
    margin: 0;
    padding: 50px 0 0 0px;
    line-height: normal;
}
		
#gwlogo h1 { 
    font-family: Georgia, "Times New Roman", Times, serif;
    font-size:40px;
}

#gwlogo img a {
    border: 0;
}

#gwlogo h1 {
    text-decoration: none;
    color: #28313A; 
}

#gwlogo h2 {
    float: left;
    padding: 65px 0 0 18px;
    font: 18px Georgia, "Times New Roman", Times, serif;
    color: #28313A; 
}

#gwlogo p  {
    text-decoration: none;
    color: #28313A;
}

#gwlogo img.logo_main {
    float: left;
    margin-top: 55px;
    border: 0;
}

/* Content */

.gwpost {
    padding: 0px 20px;
    margin-bottom: 20px;
}

#gwcontent {
    float: left;
    width: 620px;
    border-right: 1px dashed #DFE1E0;
}

#gwfooter-wrap {
}

#gwfooter {
    width: 900px;
    margin: 0 auto;
    margin-top: 20px;
    background: #E5E5E5;
    border: 0px #FFFFFF solid;
}

#gwfooter p {
    font-size: 12px;
}

#gwlegal {
    clear: both;
    padding-top: 15px;
    padding-bottom: 10px;
    text-align: center;
    color: #595959;
}

#gwlegal a {
    font-weight: normal;
    color: #1B75A9;
}
</style>

{% for css in resources.inlining.css -%}
    <style type="text/css">
    {{ css }}
    </style>
{% endfor %}

<style type="text/css">
body {
    margin: 0;
    padding: 0;
		background: #98A1AA url(data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAZABkAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQICAQECAQEBAgICAgICAgICAQICAgICAgICAgL/2wBDAQEBAQEBAQEBAQECAQEBAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgL/wgARCAC0AB4DAREAAhEBAxEB/8QAGgABAQEBAQEBAAAAAAAAAAAAAAMBBAIICf/EABYBAQEBAAAAAAAAAAAAAAAAAAACAf/aAAwDAQACEAMQAAAB/dhIAkkAc4AIAA5gAc4AIgAiADnABAGAmACADTYpBpskgCYAJqAElADAATNMBoAPAAPKdbjB9IqAH//EABcQAQEBAQAAAAAAAAAAAAAAABEAIFD/2gAIAQEAAQUCZmcszMzMzMzMzMzMzMzMzMzMzMzMzMzM8n//xAAdEQADAAICAwAAAAAAAAAAAAAAARIRIRAgMEBQ/9oACAEDAQE/AaKKK+S9C2NYJHsWhvJXhkkkn1c8UV1//8QAFBEBAAAAAAAAAAAAAAAAAAAAYP/aAAgBAgEBPwE5/8QAFBABAAAAAAAAAAAAAAAAAAAAYP/aAAgBAQAGPwI5/8QAIhAAAQQCAgMAAwAAAAAAAAAAAAERcfAh0YHhECCxMFGh/9oACAEBAAE/IZEiRIdB0HQdB9TsfU7H1Ox9TskSJEiRIkSHVUHVUHVUHVUJfCXwl8JfDkcjkciRIkS8HVPO/wDf87Krj6nY+p2SJEiXqDqOo6jqPc7Hudj3Ox7nY9zse52Pc7Hud+roOg6Dp+F1HUdR18vc6Hudev8A/9oADAMBAAIAAwAAABCSQAAAAACSSSQAAACSQSSAC2QkAAAAAACSQACCQAAACkAAD//EABwRAQADAAIDAAAAAAAAAAAAABEAAXEgMEBQUf/aAAgBAwEBPxDExMTHqaIWUQkArNSyQlkjAATHTqamprxaVgS7Ku/kxMcf/8QAFBEBAAAAAAAAAAAAAAAAAAAAYP/aAAgBAgEBPxA5/8QAJhAAAQMDBAEEAwAAAAAAAAAAAAERoVFh0XGR4fDxIDGBsSFBwf/aAAgBAQABPxB1EDqIHUQOogvQuC9C4L0LgvQuC5AXIC5AXIDs3B2bg7Nwdm4GVSMqkZVIyqTS6WNLpY0uljS6WGeOQzxyGeOQzxyNe7k17uTXu5Ne7kZVIyqRlUjKpEWqsirsgqFV04Dr7IOvsgqiN7NCSgRaftdsi5AXIB1EDqIHUQOog0TwaJ4NE8GieC9CYL0JgvQmC9CYHdUHdUHdUHdUHdUHdUHdUHdUHWq7qOtV3Udaruo61XdT5vjJrJqmC9C4L0LgZq7qv2oz+VT6GS+65GS+659N6EwXoTBehMF6EwIq/l0Ztf6iHfZV+kHUB1PSf//Z) repeat-x left top; 
    font-size: 15px;
		font-family: 'Open Sans', sans-serif;
    text-align: justify;
    color: #3C3C3C;
}
.anchor-link { visibility: hidden;}
div.prompt { display: none;}
</style>

<style type="text/css">
}
div#notebook{
margin-top:50px;
margin-bottom:100px;
}
div.cell{
max-width:55em;
margin-left:auto;
margin-right:auto;
}
div.input_prompt, div.output_prompt{
margin-left:-11ex;
}
div.input, div.output_wrapper{
margin-top:1em;
margin-bottom:1em;
}
</style>

<!-- Loading mathjax macro -->
<!-- Load mathjax -->
<script>
MathJax = {
  AuthorInit: function () {
    MathJax.HTML.getScript = function (node) {return node.textContent}
  }
};
</script>
		<script data-cfasync="false" type="text/javascript"
		src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS_HTML"></script>
    <!-- MathJax configuration -->
    <script data-cfasync="false" type="text/x-mathjax-config">
    MathJax.Hub.Config({
        tex2jax: {
            inlineMath: [ ['$','$'], ["\\(","\\)"] ],
            displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
            processEscapes: true,
            processEnvironments: true
        },
        // Center justify equations in code and markdown cells. Elsewhere
        // we use CSS to left justify single line equations in code cells.
        displayAlign: 'center',
        "HTML-CSS": {
            styles: {'.MathJax_Display': {"margin": 0}},
            linebreaks: { automatic: true }
        }
    });
    </script>
    <!-- End of mathjax configuration -->


{%- endblock header -%}
</head>


<body>
{% block body %}
<div id="gwwrapper">

<div id="gwlogo">
<a target="_blank" href="http://www.gwoptics.org">
<img class="logo_main" alt="gwoptics"  width="158" height="40" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJ4AAAAoCAMAAAA4yLMhAAAABGdBTUEAALGPC/xhBQAAAGBQTFRF/wAAAAAA/wAA/wAA/wAA/wAAAAAA/wAAAAAAAAAAAAAA/wAAAAAA/wAAAAAA/wAA/wAAAAAAAAAA/wAA/wAAAAAA/wAA/wAA/wAA/wAAAAAA/wAAhQAAAAAAAAAA/wAAMSXe1gAAAB50Uk5Tj+TEN+mnQEhWayhbhicYmNGc8G/2uhzeD7fSggkAcnzxvgAABOBJREFUWMPNmGm3oygQhnGL+4YLLij//18OVVCIuZ053ZOc6fjhXoIKD28tFLLjr1x1m9S/8xz7O3irUt0X48VKjfJ78Qal9i9W75jn48vw5H945//DY91H8OQj77HRyM96W/geXlM08K8/T8DLt5M/PkeXKrW+gVdUwamvKSv030x3PPT/7efzRb/lvqrRvnYiTEqvb15bjcNElwyLF6lPeGV85eX6eZCy7cTaDjXhZfw8g+20F6o4WU5DlVcoZcP93mNOdHplwzqquCSZ2lG1i067cMUD9tFPuNAD56FTivCWVqlw30NFg9Sh/j3odwaLV2mDFnpyoCTRAG8iDk69IGrlpItt+pqFUi3CxYCwCtEOLIQmM72jwxOaB+8om1pmTYpY0BsBrlAJ/N712PB6M7kpoXn2Ds/oqLsvVE739cCxS67UrFsESdBMJbStILrVymWZMd/tAh4yll86UInGgBZTKsWOjiHe5AkC6uTYQlNbO2YOGrrpYb3ckbxrt0s/SqC74sE+sSgrr80OgGea7bW9peEK8KTmMSBe5sWABKgHcTqS3kHDWrJrcjflTL4POrn9Cuw1/AIPEMZL1nv0jV65wA4ZWCDrhOdZGCK+kUUlP90zm71/HDosrBXshOhN0scrCfoZT/t97FQv73gw0joTXu9FQIGS2Vau73BnW3JDvRjpqg5V+xPiPDc80CZ+gSfca+kdD9akxh2dgjVepkDToqV1aztyUnIjaAwN8oTLva0PoR1veAv52PwKryOf9a72SkosO521tF/1NkQnMObDmjQ/N9LxkM4JYerxGnO3WDc88CNcwks8cTMBJfHYpEidlis3szZzUJhwqFBRaQJCp2INGlAMc/lp9dIfe9OyY36Kaza5uAUmwMslRSdH1v7sG4fXu6z3tPCXvif+FS+h2H6uBxPM74zbmWUPLJj2Ni/19bqLN4XDC5wnoF73yF2e8VzueYn3czN272oBYxYY3ytMbsYYdaUKZpZN90P8SJMNp6sa8BIw6pQcz3gtOf78RBFSYlnG59io6W2tnwDjnryfbArOsWxpXKicU34GEr3QxrBXZOn3R6rJ9U401oRHOsHciYsRcT8KWb8F+UJy4WiGhaauyknYw1YpQUbbg9vg4BfnaGhuvLHybprt0uyuRzRSdgU8IR1/Jy/XBB+bnZhEAXcE9ko2wv8xnu3bY8SMYNr7wXR+gqOqYLNm3pqm8kyLs4Qmv0u9+Y+lt52GNdZ9+i7pUoMRu7WDxxYopzTTXl/VlkiSbjRjdEqkJjtjQQW1HKyxmIyM1/RAO+HyzRp0kDwV/pChRAg2rL3dXoyaBO5421WEVQr2sFF0YdiJOLylOZXMzmHFKhDSFfMNWDKfTl+gq3gy+8mvqvtoYGwvl1sxsi/lzvbhvhvIqCyjV6W+fjx1R0tZpwMbUnkV87LiaODtqubA1bLmot+2qvmd46L6zRP2H5w1wOm2wuiVv3ma/TierFy83k4S34H30Jk5eLiivfguvMyFJ24a/PgqPDgabvJKdNW733b8re59vMxzt+ZnZvvjK1L37etNvMpzt/483/1uEeEZ9vo88An1cqLjb2YVLKvwqFB+yvegouofstA7xla8O1yaRnVdR1E6fypyC06fVvqPfjH7VN6T+RTwqcqK4/uufwCXLKKJjiOZSwAAAABJRU5ErkJggg=="></a>
<h2> &raquo;&nbsp;&nbsp;&nbsp;Tools for detecting gravitational waves</h2>
<br/><br/>
</div>

<div id="gwheader">
<div id="gwmenu">
<ul>
<li><a title="gwoptics start page" href="/">Home</a></li>
%%%%LEARN_REPLACE%%%%
%%%%TOC_REPLACE%%%%
</li>
<li><a title="Games and apps for science outreach" href="/play/">Play</a>
<ul>
	<li class="sep"><a href="/play/">Play Home</a></li>
	<li class="sep"><a target="_blank" href="https://www.laserlabs.org">Laser Labs</a></li>
	<li class="sep"><a target="_blank" href="https://www.laserlabs.org/pocketblackhole.php">Pocket Black Hole</a></li>
	<li><a target="_blank" href="https://www.laserlabs.org/stretchandsquash.php">Stretch and Squash</a></li>
	<li class="sep"><a href="/processing/space_time_quest/">Space Time Quest</a></li>
	<li><a target="_blank" href="https://www.laserlabs.org/blackholemaster.php">Black
	Hole Master</a></li>
	<li class="sep"><a href="/processing">Processing Sketches</a></li>
</ul>
</li>
<li><a title="Optical simulations and software tools" href="/research/">Simulations</a>
<ul>
	<li class="sep"><a href="/research/">Simulation Home</a></li>
	<li class="sep"><a href="/finesse">Finesse Main Page</a></li>
	<li><a href="/finesse/reference">Finesse Syntax</a></li>
	<li class="sep"><a href="/pykat">PyKat Main Page</a></li>
	<li class="sep"><a href="/simtools">Simtools (Matlab)</a></li>
	<li><a href="/ComponentLibrary">ComponentLibrary</a></li>
</ul>
</li>
<li><a target="_blank" title="Contact and license information" href="http://www.gwoptics.org/contact/">Contact</a></li>
<li class="last">
<a title="gwoptics on Twitter" target="_blank" class="last" href="http://www.twitter.com/gwoptics">
<img  width="22" height="22" alt="Follow gwoptics on Twitter" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAMAAADzapwJAAAABGdBTUEAALGPC/xhBQAAAZtQTFRFCXGhCXGhCXGhCXGhCXGhCXGhCXGhCXGhAAAACXGhMZ/G7PL1hcrhVp6+K5bAudTfXq/OJJC7I465T7fYL5zDmcja4O7zIIy3HIay0t/lgMXdOKfMSLjautXfibjMtd7sS6LFLprDMI20Y7bTF4GuaavHQpi8KJO8jcPXH4m1er7Wrs/dmtHj5OvtWrzavNfiGIKv0OXsa73ZKZS+8fj6gsfem8PUwdTdKJS+0uDlHoi0K4+31uTpO6nOGYOwPKvPL53ENZm/IIq2ic/lGoSwa77axtriLJnBP5W5R7fZG4WydcDa3eTnQrHUSJ7CNKLIOKXLerPL7vT3Hom1OqnOIYu3SLfZoNjqJI+5NqTKJZK8RKPHRbXYFoCtGIGuFH2rLJjBHIazJ5S9vd/rL5vDO6rPsczXH4q1MZ/G6fDyMJzEOabMPq3RQK/TNqPJ+vr6IYy3MqDHKpa//f39QbDU7e3tLZnC8PDw6+vr8vLyJ5O96enpJZC69/f39fX1Io24RLPWHoi1T7/gRrbZS7vdTb7eSbnbIIu2CXGhzU6TAQAAAAp0Uk5TJ/DzqCrtG+YArbkUyxwAAAE0SURBVBjTbdFVU8NgEIXhr5YmM7i7u7u7O1SouzfSpm0IUBII2vxsNs0MTCnP1dn3dhGO6YxyCaMOwxEy8La3EjbeoEdEw2cZkkCa048yHVokf/1DRvL7L8++3e5RBmRJkqbqJcVld27hnFEWZI5jDnPhCoZjFnNgjuE4DjJNb1/XmNPmifamNAhv0jQNORq1Ot1JURRnRUWyv80ahUxR1E3kKvn8Y8xJQU6BxO745KNqY3okkYKcAYnj5up71WA8tJOBTEYa3WTvsOmuqLUwH4iQkPmqntWjzgfVxZArwPM85OyKY33pSbV8woayAHI+72LP+kyxWKyrciZem1dAFgTBwa4d+AZ8Wy2FOqFIRprbF8DujVos8eJULi0ivIUyXgLpDf7ga4mgH56GY8TfFxMY/g0I3cOIgOCpYQAAAABJRU5ErkJggg==" /></a>
</li>
</ul>
</div>
</div>
</div>

<div id="gwpage">
<h1 class="course-title">Course: Learn Laser Interferometry with Finesse</h1>
<hr />
{{ super() }}


<div style="clear: both;">&nbsp;</div>
<div id="gwfooter">
<p id="gwlegal">&copy; Andreas Freise 2009 onwards. The css design is based on a free template from <a href="http://www.freecsstemplates.org/">Free CSS Templates</a>.</p>
</div>
</div>
 
{%- endblock body %}
</body>


{% block footer %}
</html>
{% endblock footer %}
