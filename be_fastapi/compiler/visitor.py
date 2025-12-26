from antlr.compiled_files.GuildFlowVisitor import GuildFlowVisitor
from antlr.compiled_files.GuildFlowParser import GuildFlowParser
from app.schemas.compiler import (
    WorkflowSchema, 
    ActionSchema, 
    IfBlockSchema, 
    StateSchema,
    TransitionSchema,
    SetVarSchema,
    ComponentSchema
)

class GuildFlowCompiler(GuildFlowVisitor):
    def visitProg(self, ctx: GuildFlowParser.ProgContext):
        """Return a list of workflow and state definitions"""
        return [self.visit(child) for child in ctx.definition()]
    
    def visitDefinition(self, ctx: GuildFlowParser.DefinitionContext):
        """Visit either workflow_def or state_def"""
        if ctx.workflow_def():
            return self.visit(ctx.workflow_def())
        elif ctx.state_def():
            return self.visit(ctx.state_def())
        return None
    
    def visitWorkflow_def(self, ctx: GuildFlowParser.Workflow_defContext):
        """Process workflow definition with name, trigger, optional condition, and steps"""
        steps = [self.visit(step) for step in ctx.statement()]
        
        return WorkflowSchema(
            name=ctx.IDENTIFIER().getText(),
            trigger=self.visit(ctx.event_type()),
            condition=self.visit(ctx.condition()) if ctx.condition() else None,
            steps=[step for step in steps if step]
        ).model_dump()
    
    def visitEvent_type(self, ctx: GuildFlowParser.Event_typeContext):
        """Return event type as string"""
        return ctx.IDENTIFIER().getText()
    
    def visitState_def(self, ctx: GuildFlowParser.State_defContext):
        """Process state definition with name and steps"""
        steps = [self.visit(step) for step in ctx.statement()]
        
        return StateSchema(
            name=ctx.IDENTIFIER().getText(),
            steps=[step for step in steps if step]
        ).model_dump()
    
    def visitStatement(self, ctx: GuildFlowParser.StatementContext):
        """Route to appropriate statement type"""
        if ctx.action_statement():
            return self.visit(ctx.action_statement())
        elif ctx.if_statement():
            return self.visit(ctx.if_statement())
        elif ctx.transition_statement():
            return self.visit(ctx.transition_statement())
        elif ctx.component_statement():
            return self.visit(ctx.component_statement())
        elif ctx.set_statement():
            return self.visit(ctx.set_statement())
        elif ctx.extract_statement():
            return self.visit(ctx.extract_statement())
        return None
        
    def visitAction_statement(self, ctx: GuildFlowParser.Action_statementContext):
        """Process action with command and parameters"""
        command = self.visit(ctx.command())
        params = {}
        
        for param in ctx.param():
            key = param.IDENTIFIER().getText()
            value = self.visit(param.expr())
            params[key] = value
            
        return ActionSchema(
            command=command, 
            params=params
        ).model_dump()
    
    def visitCommand(self, ctx: GuildFlowParser.CommandContext):
        """Return command name"""
        return ctx.getText()
    
    def visitParam(self, ctx: GuildFlowParser.ParamContext):
        """Process parameter - handled in visitAction_statement"""
        return self.visitChildren(ctx)
        
    def visitIf_statement(self, ctx: GuildFlowParser.If_statementContext):
        """Process if-else statement with condition and branches"""
        condition = self.visit(ctx.condition())
        
        # Get then_block statements
        then_steps = [self.visit(stmt) for stmt in ctx.then_block]
        
        # Get else_block statements if exists
        else_steps = [self.visit(stmt) for stmt in ctx.else_block] if ctx.else_block else []
        
        return IfBlockSchema(
            condition=condition,
            then_branch=[step for step in then_steps if step],
            else_branch=[step for step in else_steps if step]
        ).model_dump()
    
    def visitCondition(self, ctx: GuildFlowParser.ConditionContext):
        """Build condition object with left, operator, right"""
        left = self.visit(ctx.expr(0))
        operator = self.visit(ctx.comparator())
        right = self.visit(ctx.expr(1))
        
        return {
            "left": left,
            "operator": operator,
            "right": right
        }
    
    def visitComparator(self, ctx: GuildFlowParser.ComparatorContext):
        """Return comparator operator"""
        return ctx.getText()
    
    def visitTransition_statement(self, ctx: GuildFlowParser.Transition_statementContext):
        """Process state transition"""
        target_state = ctx.IDENTIFIER().getText()
        
        return TransitionSchema(
            target_state=target_state
        ).model_dump()
    
    def visitComponent_statement(self, ctx: GuildFlowParser.Component_statementContext):
        """Process UI components list"""
        elements = [self.visit(elem) for elem in ctx.component_element()]
        
        # Return all component elements as a list
        return {
            "type": "UI_COMPONENTS",
            "components": elements
        }
    
    def visitComponent_element(self, ctx: GuildFlowParser.Component_elementContext):
        """Process individual component with type and props"""
        component_type = self.visit(ctx.component_type())
        props = {}
        
        for prop in ctx.component_prop():
            key = self.visit(prop.prop_key())
            value = self.visit(prop.expr())
            props[key] = value
        
        return ComponentSchema(
            component_type=component_type,
            props=props
        ).model_dump()
    
    def visitComponent_type(self, ctx: GuildFlowParser.Component_typeContext):
        """Return component type name"""
        return ctx.IDENTIFIER().getText()
    
    def visitComponent_prop(self, ctx: GuildFlowParser.Component_propContext):
        """Process component property - handled in visitComponent_element"""
        return self.visitChildren(ctx)
    
    def visitProp_key(self, ctx: GuildFlowParser.Prop_keyContext):
        """Return property key name"""
        return ctx.IDENTIFIER().getText()
    
    def visitSet_statement(self, ctx: GuildFlowParser.Set_statementContext):
        """Process variable assignment"""
        variable = self.visit(ctx.variable())
        value = self.visit(ctx.expr())
        
        # Extract variable name from dict if it's a variable object
        var_name = variable["name"] if isinstance(variable, dict) else variable
        
        return SetVarSchema(
            variable=var_name,  # Pass string, not dict
            value=value
        ).model_dump()
    
    def visitExtract_statement(self, ctx: GuildFlowParser.Extract_statementContext):
        """Process field extraction to variable"""
        variable = self.visit(ctx.variable())
        field_name = ctx.IDENTIFIER().getText()
        
        # Extract variable name from dict
        var_name = variable["name"] if isinstance(variable, dict) else variable
        
        return SetVarSchema(
            variable=var_name,  # Pass string, not dict
            value={"type": "extract_field", "field": field_name}
        ).model_dump()
    
    def visitExpr(self, ctx: GuildFlowParser.ExprContext):
        """Handle different expression types"""
        if ctx.value():
            return self.visit(ctx.value())
        elif ctx.variable():
            return self.visit(ctx.variable())
        elif ctx.expr():  # Parenthesized expression
            return self.visit(ctx.expr(0))
        return None
    
    def visitVariable(self, ctx: GuildFlowParser.VariableContext):
        """Return variable reference with dot notation support"""
        # Get all identifiers for dot notation (e.g., user.name)
        identifiers = [id_node.getText() for id_node in ctx.IDENTIFIER()]
        var_path = '.'.join(identifiers)
        
        return {
            "type": "variable",
            "name": var_path
        }
    
    def visitValue(self, ctx: GuildFlowParser.ValueContext):
        """Return the actual value (string, number, boolean, array, object)"""
        if ctx.STRING():
            # Remove quotes from string
            text = ctx.STRING().getText()
            return text[1:-1]  # Strip quotes
        elif ctx.NUMBER():
            text = ctx.NUMBER().getText()
            # Parse as int or float
            if '.' in text or 'e' in text.lower():
                return float(text)
            return int(text)
        elif ctx.getText() == 'TRUE':
            return True
        elif ctx.getText() == 'FALSE':
            return False
        elif ctx.array_literal():
            return self.visit(ctx.array_literal())
        elif ctx.object_literal():
            return self.visit(ctx.object_literal())
        
        return None
    
    def visitArray_literal(self, ctx: GuildFlowParser.Array_literalContext):
        """Return array of expressions"""
        if not ctx.expr():
            return []
        return [self.visit(expr) for expr in ctx.expr()]
    
    def visitObject_literal(self, ctx: GuildFlowParser.Object_literalContext):
        """Return dictionary/object from component_prop list"""
        obj = {}
        
        if ctx.component_prop():
            for prop in ctx.component_prop():
                key = self.visit(prop.prop_key())
                value = self.visit(prop.expr())
                obj[key] = value
        
        return obj