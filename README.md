##VIVO sample data

August 3, 2014

This repository contains sample data that can be loaded into the [VIVO](http://vivoweb.org/) Semantic Web application.

This is intended to be a basic sample set of data that can be loaded into a fresh VIVO instance.  See the [VIVO Vagrant](https://github.com/lawlesst/vivo-vagrant) and [background information](https://wiki.duraspace.org/display/VIVO/Learning+about+VIVO) if you are interested in getting started with VIVO.

The data is mapped to the [VIVO ISF](https://wiki.duraspace.org/display/VIVO/VIVO-ISF+Ontology) ontology.  The VIVO ISF was introduced in VIVO version 1.6.


###Contents

 * [People](data/csv/people.csv)
 * [Organizations](data/csv/organizations.csv)
 * [Positions](data/csv/positions.csv)

###Loading the data
With a VIVO instance running at `http://localhost:8080/vivo/` login as an administrative user.  Go to Site Admin (top right hand corner) and click "Add/Remove RDF data".  Then upload the `all.ttl` file and select "Turtle from the dropdown menu."

![ScreenShot](tutorial/images/add_remove_rdf.png)

After loading the data visit `http://localhost:8080/vivo/display/org102017` in your browser, assuming you are running VIVO locally.  This is the sample "Geothermal Technology Department" and has several members that you can browse.