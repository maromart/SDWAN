import json
import os.path

__author__ = "Mario Uriel Romero Martinez"
__version__ = "1.0"
__maintainer__ = "Mario Uriel Romero Martinez"


def find_greatest(xlist):

    return max(xlist)


def create_html(jsonfile,htmlfilename,dtq,dq):

    print(dtq)
    print(dq)
    

    maxdt=find_greatest(dtq)
    maxd=find_greatest(dq)


    if maxdt>100 or maxd>100:
        w=5000
        h=3500
        dpt=1000
    
    elif maxdt<=20 or maxd<=20:
        w=1900
        h=900
        dpt=500

    else:
        w=3000
        h=1800
        dpt=800

    path="lptreeData.json"
    check_file=os.path.isfile(path)
    if check_file:

        print("Creating HTML file")
        
        with open(jsonfile,'r') as jfile:
            pjfile=jfile.read()
            ppfile=json.loads(pjfile)
        
        fpjfile=json.dumps(ppfile,indent=4)
        #print(fpjfile)

        f = open(htmlfilename, 'w') 
        
        # the html code which will go in the file SD-WAN_Localized_Policies.html 
        html_template = """ 
        <!DOCTYPE html>
        <meta charset="UTF-8">
        <style>

       
        body {
                background-color: black;
            }
            
        .node circle {
        fill: #fff;
        stroke: steelblue;
        stroke-width: 3px;
        }

        .node text {
        font: 12px sans-serif;
        stroke: white;
        }

        .link {
        fill: none;
        stroke: rgb(21, 177, 224);
        stroke-width: 2px;
        }

                
        .sidebar {
        height: 100%%;
        width: 0;
        position: fixed;
        z-index: 1;
        top: 0;
        right: 0;
        background-color: rgb(21, 177, 224);
        overflow-x: hidden;
        transition: 0.5s;
        padding-top: 60px;
        opacity: .9;
        }

        .sidebar p {
        padding: 8px 8px 8px 32px;
        text-decoration: none;
        font:18px sans-serif;
        color: rgb(21, 177, 224);
        display: block;
        transition: 0.3s;
        background-color:black;
        box-shadow: rgba(248, 248, 248, 0.3) 0px 19px 38px, rgba(26, 173, 173, 0.22) 0px 15px 12px;
        }

        </style>

        <body>

        <div id="mySidebar" class="sidebar">
        </div>

        <!-- load the d3.js library -->	
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <script>
        var treeData = %s;

        // Set the dimensions and margins of the diagram
        var margin = {top: 20, right: 90, bottom: 30, left: 190},
            width = %s - margin.left - margin.right,
            height = %s - margin.top - margin.bottom;


        var div = d3.select("body").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

        // append the svg object to the body of the page
        // appends a 'group' element to 'svg'
        // moves the 'group' element to the top left margin
        var svg = d3.select("body").append("svg")
            .attr("width", width + margin.right + margin.left)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", "translate("
                + margin.left + "," + margin.top + ")");

        var i = 0,
            duration = 750,
            root;

        // declares a tree layout and assigns the size
        var treemap = d3.tree().size([height, width]);

        // Assigns parent, children, height, depth
        root = d3.hierarchy(treeData, function(d) { return d.children; });
        root.x0 = height / 2;
        root.y0 = 0;

        // Collapse after the second level
        root.children.forEach(collapse);

        update(root);

        // Collapse the node and all it's children
        function collapse(d) {
        if(d.children) {
            d._children = d.children
            d._children.forEach(collapse)
            d.children = null
        }
        }

        function update(source) {

        // Assigns the x and y position for the nodes
        var treeData = treemap(root);

        // Compute the new tree layout.
        var nodes = treeData.descendants(),
            links = treeData.descendants().slice(1);

        // Normalize for fixed-depth.
        nodes.forEach(function(d){ d.y = d.depth * %s});

        // ****************** Nodes section ***************************

        // Update the nodes...
        var node = svg.selectAll('g.node')
            .data(nodes, function(d) {return d.id || (d.id = ++i); });

        // Enter any new modes at the parent's previous position.
        var nodeEnter = node.enter().append('g')
            .attr('class', 'node')
            .attr("transform", function(d) {
                return "translate(" + source.y0 + "," + source.x0 + ")";
            })
            .on('click', click)
            //.on('mouseover',mouseover)
            //.on('mouseout',mouseout);

        // Add Circle for the nodes
        /*nodeEnter.append('circle')
            .attr('class', 'node')
            .attr('r', 1e-6)
            .style("fill", function(d) {
                return d._children ? "lightsteelblue" : "#fff";
            });

        */
        nodeEnter.append("path")
        .attr('class', 'node')
        .style("stroke", function(d) {return  "lightblue";})
        .style("fill", function(d) {return  d.data.wcol;})
        .attr('cursor', 'pointer') 
        .attr("d", d3.symbol()
            .size(function(d) { return 300; } )
            .type(function(d) { { return d3.symbolSquare; } 
            }));



        // Add labels for the nodes
        nodeEnter.append('text')
            .attr("dy", ".35em")
            .attr("x", function(d) {
                return d.children || d._children ? -13 : 13;
            })
            .attr("text-anchor", function(d) {
                return d.children || d._children ? "end" : "start";
            })
            .on('mouseover',mouseover)
            .on('mouseout',mouseout)
            .text(function(d) { return d.data.name; });

        // UPDATE
        var nodeUpdate = nodeEnter.merge(node);

        // Transition to the proper position for the node
        nodeUpdate.transition()
            .duration(duration)
            .attr("transform", function(d) { 
                return "translate(" + d.y + "," + d.x + ")";
            });

        // Update the node attributes and style
        nodeUpdate.select('circle.node')
            .attr('r', 10)
            .style("fill", function(d) {
                return d._children ? "lightsteelblue" : "#fff";
            })
            .attr('cursor', 'pointer');


        // Remove any exiting nodes
        var nodeExit = node.exit().transition()
            .duration(duration)
            .attr("transform", function(d) {
                return "translate(" + source.y + "," + source.x + ")";
            })
            .remove();

        // On exit reduce the node circles size to 0
        nodeExit.select('circle')
            .attr('r', 1e-6);

        // On exit reduce the opacity of text labels
        nodeExit.select('text')
            .style('fill-opacity', 1e-6);

        // ****************** links section ***************************

        // Update the links...
        var link = svg.selectAll('path.link')
            .data(links, function(d) { return d.id; });

        // Enter any new links at the parent's previous position.
        var linkEnter = link.enter().insert('path', "g")
            .attr("class", "link")
            .attr('d', function(d){
                var o = {x: source.x0, y: source.y0}
                return diagonal(o, o)
            });

        // UPDATE
        var linkUpdate = linkEnter.merge(link);

        // Transition back to the parent element position
        linkUpdate.transition()
            .duration(duration)
            .attr('d', function(d){ return diagonal(d, d.parent) });

        // Remove any exiting links
        var linkExit = link.exit().transition()
            .duration(duration)
            .attr('d', function(d) {
                var o = {x: source.x, y: source.y}
                return diagonal(o, o)
            })
            .remove();

        // Store the old positions for transition.
        nodes.forEach(function(d){
            d.x0 = d.x;
            d.y0 = d.y;
        });

        // Creates a curved (diagonal) path from parent to the child nodes
        function diagonal(s, d) {

            path = `M ${s.y} ${s.x}
                    C ${(s.y + d.y) / 2} ${s.x},
                    ${(s.y + d.y) / 2} ${d.x},
                    ${d.y} ${d.x}`

            return path
        }

        // Toggle children on click.
        function click(event, d) {
            if (d.children) {
                d._children = d.children;
                d.children = null;
            } else {
                d.children = d._children;
                d._children = null;
            }
            update(d);
        }

         function mouseover(event, d) {
       //d.nodeEnter.style('text-shadow',"1px 1px 2px black, 0 0 25px white, 0 0 5px steelblue");
        document.getElementById("mySidebar").style.width = "350px";
        const div = document.getElementById("mySidebar");
        if (d.data.wcol=='purple'){
            const a=d.data.lptypes;
            
            a.forEach((element) => {
                const para = document.createElement("p");
                const ptext1 = document.createTextNode("Type: " +Object.keys(element));
                const lbk1=document.createElement("br");
                const ptext2 = document.createTextNode("Name: " +Object.values(element));
                const lbk2=document.createElement("br");

                para.appendChild(ptext1); 
                para.appendChild(lbk1);
                para.appendChild(ptext2);
      

                div.appendChild(para);
                });}
        
        else if (d.data.wcol=='steelblue'){
            const para = document.createElement("p");

            const ptext1 = document.createTextNode(d.data.name);
            const lbk1=document.createElement("br");
            const ptext2 = document.createTextNode("System IP: " +d.data.sip);  
            const lbk2=document.createElement("br");
            const ptext3 = document.createTextNode("Site ID: " +d.data.siteid);
            
            para.appendChild(ptext1); 
            para.appendChild(lbk1);
            para.appendChild(ptext2);
            para.appendChild(lbk2);
            para.appendChild(ptext3);
            div.appendChild(para);
            
        }

            }
        
        function mouseout(event, d) {
        document.getElementById("mySidebar").style.width = "0";
        document.getElementById("mySidebar").innerHTML="";
    
       
        }
    }


        </script>
        </body>
        """ % (fpjfile,w,h,dpt)
        
        # writing the code into the file 
        f.write(html_template) 
        
        # close the file 
        f.close() 
    else:
        print("Unable to create html file, check if lptreeData.json exists in the local directory")

