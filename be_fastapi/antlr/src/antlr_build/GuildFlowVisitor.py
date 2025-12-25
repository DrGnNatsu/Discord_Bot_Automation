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


    # Visit a parse tree produced by GuildFlowParser#workflow_def.
    def visitWorkflow_def(self, ctx:GuildFlowParser.Workflow_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#state_def.
    def visitState_def(self, ctx:GuildFlowParser.State_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#state_body.
    def visitState_body(self, ctx:GuildFlowParser.State_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#statement.
    def visitStatement(self, ctx:GuildFlowParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#action_statement.
    def visitAction_statement(self, ctx:GuildFlowParser.Action_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#action_command.
    def visitAction_command(self, ctx:GuildFlowParser.Action_commandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#action_type.
    def visitAction_type(self, ctx:GuildFlowParser.Action_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#param_list.
    def visitParam_list(self, ctx:GuildFlowParser.Param_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#param.
    def visitParam(self, ctx:GuildFlowParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#value.
    def visitValue(self, ctx:GuildFlowParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#if_statement.
    def visitIf_statement(self, ctx:GuildFlowParser.If_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#condition.
    def visitCondition(self, ctx:GuildFlowParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#comparison_op.
    def visitComparison_op(self, ctx:GuildFlowParser.Comparison_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#expression.
    def visitExpression(self, ctx:GuildFlowParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#set_statement.
    def visitSet_statement(self, ctx:GuildFlowParser.Set_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#extract_stmt.
    def visitExtract_stmt(self, ctx:GuildFlowParser.Extract_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#components_block.
    def visitComponents_block(self, ctx:GuildFlowParser.Components_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#component.
    def visitComponent(self, ctx:GuildFlowParser.ComponentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GuildFlowParser#button_property.
    def visitButton_property(self, ctx:GuildFlowParser.Button_propertyContext):
        return self.visitChildren(ctx)



del GuildFlowParser