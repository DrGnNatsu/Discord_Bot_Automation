# Generated from GuildFlow.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GuildFlowParser import GuildFlowParser
else:
    from GuildFlowParser import GuildFlowParser

# This class defines a complete generic visitor for a parse tree produced by GuildFlowParser.

class GuildFlowVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GuildFlowParser#prog.
    def visitProg(self, ctx:GuildFlowParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#definition.
    def visitDefinition(self, ctx:GuildFlowParser.DefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#workflow_def.
    def visitWorkflow_def(self, ctx:GuildFlowParser.Workflow_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#event_type.
    def visitEvent_type(self, ctx:GuildFlowParser.Event_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#state_def.
    def visitState_def(self, ctx:GuildFlowParser.State_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#statement.
    def visitStatement(self, ctx:GuildFlowParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#action_statement.
    def visitAction_statement(self, ctx:GuildFlowParser.Action_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#command.
    def visitCommand(self, ctx:GuildFlowParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#param.
    def visitParam(self, ctx:GuildFlowParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#if_statement.
    def visitIf_statement(self, ctx:GuildFlowParser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#condition.
    def visitCondition(self, ctx:GuildFlowParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#comparator.
    def visitComparator(self, ctx:GuildFlowParser.ComparatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#transition_statement.
    def visitTransition_statement(self, ctx:GuildFlowParser.Transition_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#component_statement.
    def visitComponent_statement(self, ctx:GuildFlowParser.Component_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#component_element.
    def visitComponent_element(self, ctx:GuildFlowParser.Component_elementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#component_type.
    def visitComponent_type(self, ctx:GuildFlowParser.Component_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#component_prop.
    def visitComponent_prop(self, ctx:GuildFlowParser.Component_propContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#prop_key.
    def visitProp_key(self, ctx:GuildFlowParser.Prop_keyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#set_statement.
    def visitSet_statement(self, ctx:GuildFlowParser.Set_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#extract_statement.
    def visitExtract_statement(self, ctx:GuildFlowParser.Extract_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#expr.
    def visitExpr(self, ctx:GuildFlowParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#variable.
    def visitVariable(self, ctx:GuildFlowParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#value.
    def visitValue(self, ctx:GuildFlowParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#array_literal.
    def visitArray_literal(self, ctx:GuildFlowParser.Array_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#object_literal.
    def visitObject_literal(self, ctx:GuildFlowParser.Object_literalContext):
        return self.visitChildren(ctx)



del GuildFlowParser