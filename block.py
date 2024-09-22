from blockdiag import parser, builder, drawer

# Create the diagram definition
diagram_text = """
blockdiag {
  A -> B -> C;
  A -> D;
  D -> C;
}
"""

# Parse the diagram definition
tree = parser.parse_string(diagram_text)

# Build the diagram
diagram = builder.ScreenNodeBuilder.build(tree)

# Draw the diagram
drawer = drawer.DiagramDraw('PNG', diagram, filename='example_diagram.png')
drawer.draw()
drawer.save()