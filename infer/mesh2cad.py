import trimesh
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Sewing
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Extend.DataExchange import write_step_file
from OCC.Core.TopoDS import TopoDS_Builder
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon

mesh = trimesh.load("./ft_generated_results_v1/gt/T8_sample_000.glb")

builder = BRep_Builder()
compound = TopoDS_Compound()
builder.MakeCompound(compound)

for face in mesh.faces:
    pts = [mesh.vertices[i] for i in face]
    poly = BRepBuilderAPI_MakePolygon()
    for p in pts:
        poly.Add(gp_Pnt(*p))
    poly.Close()

    face = BRepBuilderAPI_MakeFace(poly.Wire()).Face()
    builder.Add(compound, face)

# write to cad
write_step_file(compound, "./output.step")
