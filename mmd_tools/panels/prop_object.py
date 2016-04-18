# -*- coding: utf-8 -*-

import bpy
from bpy.types import Panel

import mmd_tools.core.model as mmd_model


class _PanelBase(object):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'


class MMDModelObjectPanel(_PanelBase, Panel):
    bl_idname = 'OBJECT_PT_mmd_tools_root_object'
    bl_label = 'MMD Model Information'

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if obj is None:
            return False

        root = mmd_model.Model.findRoot(obj)
        if root is None:
            return False

        return True

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        root = mmd_model.Model.findRoot(obj)

        c = layout.column()
        c.prop(root.mmd_root, 'name')
        c.prop(root.mmd_root, 'name_e')
        c.prop(root.mmd_root, 'scale')
        c = layout.column()
        c.prop_search(root.mmd_root, 'comment_text', search_data=bpy.data, search_property='texts')
        c.prop_search(root.mmd_root, 'comment_e_text', search_data=bpy.data, search_property='texts')


class MMDRigidPanel(_PanelBase, Panel):
    bl_idname = 'RIGID_PT_mmd_tools_bone'
    bl_label = 'MMD Rigidbody'

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.mmd_type == 'RIGID_BODY'

    def draw(self, context):
        obj = context.active_object

        layout = self.layout
        c = layout.column()
        c.prop(obj, 'name')
        c.prop(obj.mmd_rigid, 'name_e')

        c = layout.column(align=True)
        row = c.row(align=True)
        row.prop(obj.mmd_rigid, 'type', expand=True)

        root = mmd_model.Model.findRoot(obj)
        relation = obj.constraints.get('mmd_tools_rigid_parent')
        if root is None:
            row = c.row(align=True)
            row.enabled = False
            if relation is not None:
                row.prop(relation, 'subtarget', text='', icon='BONE_DATA')
            else:
                row.prop(obj.mmd_rigid, 'bone', text='', icon='BONE_DATA')
        else:
            row = c.row(align=True)
            armature = mmd_model.Model(root).armature()
            if relation is not None:
                row.prop_search(relation, 'subtarget', text='', search_data=armature.pose, search_property='bones', icon='BONE_DATA')
            else:
                row.prop_search(obj.mmd_rigid, 'bone', text='', search_data=armature.pose, search_property='bones', icon='BONE_DATA')

        row = layout.row()

        c = row.column()
        if obj.rigid_body is None:
            c.operator(bpy.ops.rigidbody.object_add.idname(), icon='MESH_ICOSPHERE')
            return

        c.prop(obj.rigid_body, 'mass')
        c.prop(obj.mmd_rigid, 'collision_group_number')
        c = row.column()
        c.prop(obj.rigid_body, 'restitution', text='Bounciness')
        c.prop(obj.rigid_body, 'friction')

        c = layout.column()
        c.prop(obj.mmd_rigid, 'collision_group_mask')

        c = layout.column()
        c.label('Damping')
        row = c.row()
        row.prop(obj.rigid_body, 'linear_damping')
        row.prop(obj.rigid_body, 'angular_damping')


class MMDJointPanel(_PanelBase, Panel):
    bl_idname = 'JOINT_PT_mmd_tools_bone'
    bl_label = 'MMD Joint Tools'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'object'

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.mmd_type == 'JOINT'

    def draw(self, context):
        obj = context.active_object
        rbc = obj.rigid_body_constraint

        layout = self.layout
        c = layout.column()
        c.prop(obj.mmd_joint, 'name_j')
        c.prop(obj.mmd_joint, 'name_e')

        c = layout.column()
        if rbc is None:
            c.operator(bpy.ops.rigidbody.constraint_add.idname(), icon='CONSTRAINT')
        else:
            c.prop(rbc, 'object1')
            c.prop(rbc, 'object2')

            row = layout.row(align=True)
            col = row.column(align=True)
            col.label('X-Axis:')
            col.label('Y-Axis:')
            col.label('Z-Axis:')
            col = row.column(align=True)
            row = col.row(align=True)
            row.prop(rbc, 'limit_lin_x_lower')
            row.prop(rbc, 'limit_lin_x_upper')
            row = col.row(align=True)
            row.prop(rbc, 'limit_lin_y_lower')
            row.prop(rbc, 'limit_lin_y_upper')
            row = col.row(align=True)
            row.prop(rbc, 'limit_lin_z_lower')
            row.prop(rbc, 'limit_lin_z_upper')

            row = layout.row(align=True)
            col = row.column(align=True)
            col.label('X-Axis:')
            col.label('Y-Axis:')
            col.label('Z-Axis:')
            col = row.column(align=True)
            row = col.row(align=True)
            row.prop(rbc, 'limit_ang_x_lower')
            row.prop(rbc, 'limit_ang_x_upper')
            row = col.row(align=True)
            row.prop(rbc, 'limit_ang_y_lower')
            row.prop(rbc, 'limit_ang_y_upper')
            row = col.row(align=True)
            row.prop(rbc, 'limit_ang_z_lower')
            row.prop(rbc, 'limit_ang_z_upper')

        col = layout.column()
        row = col.row()
        row.column(align=True).prop(obj.mmd_joint, 'spring_linear')
        row.column(align=True).prop(obj.mmd_joint, 'spring_angular')

