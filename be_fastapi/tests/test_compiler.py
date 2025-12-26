import pytest
from compiler.compiler import compile_code, CompilerError

class TestGuildFlowCompiler:
    """Test suite for GuildFlow compiler"""
    
    def test_simple_workflow(self):
        """Test compiling a simple workflow with action"""
        source = """
        WORKFLOW WelcomeFlow ON MEMBER_JOIN {
            ACTION: SEND_MESSAGE channel="welcome" content="Hello!"
        }
        """
        
        result = compile_code(source)
        
        assert len(result) == 1
        workflow = result[0]
        assert workflow["type"] == "WORKFLOW"
        assert workflow["name"] == "WelcomeFlow"
        assert workflow["trigger"] == "MEMBER_JOIN"
        assert len(workflow["steps"]) == 1
        assert workflow["steps"][0]["type"] == "ACTION"
        assert workflow["steps"][0]["command"] == "SEND_MESSAGE"
    
    def test_workflow_with_condition(self):
        """Test workflow with WHERE condition"""
        source = """
        WORKFLOW ModFlow ON MESSAGE_CREATE WHERE user.role == "mod" {
            ACTION: BAN_USER user=message.author
        }
        """
        
        result = compile_code(source)
        workflow = result[0]
        
        assert workflow["condition"] is not None
        assert workflow["condition"]["operator"] == "=="
        assert workflow["condition"]["left"]["type"] == "variable"
        assert workflow["condition"]["left"]["name"] == "user.role"
    
    def test_if_statement(self):
        """Test if-else statement"""
        source = """
        WORKFLOW CheckFlow ON MESSAGE_CREATE {
            IF message.content contains "bad" {
                ACTION: TIMEOUT_USER user=message.author duration=60
            } ELSE {
                ACTION: REPLY_MESSAGE content="All good!"
            }
        }
        """
        
        result = compile_code(source)
        workflow = result[0]
        
        assert len(workflow["steps"]) == 1
        if_block = workflow["steps"][0]
        assert if_block["type"] == "LOGIC_IF"
        assert len(if_block["then_branch"]) == 1
        assert len(if_block["else_branch"]) == 1
    
    def test_set_statement(self):
        """Test SET variable statement"""
        source = """
        WORKFLOW VarFlow ON MESSAGE_CREATE {
            SET counter = 10
            SET user_name = "TestUser"
        }
        """
        
        result = compile_code(source)
        workflow = result[0]
        
        assert len(workflow["steps"]) == 2
        assert workflow["steps"][0]["type"] == "SET_VAR"
        assert workflow["steps"][0]["value"] == 10
        assert workflow["steps"][1]["value"] == "TestUser"
    
    def test_transition_statement(self):
        """Test ENTER_STATE transition"""
        source = """
        WORKFLOW TransitionFlow ON BUTTON_CLICK {
            ENTER_STATE WaitingState
        }
        """
        
        result = compile_code(source)
        workflow = result[0]
        
        assert len(workflow["steps"]) == 1
        assert workflow["steps"][0]["type"] == "TRANSITION"
        assert workflow["steps"][0]["target_state"] == "WaitingState"
    
    def test_component_statement(self):
        """Test UI component definition"""
        source = """
        WORKFLOW UIFlow ON MESSAGE_CREATE {
            COMPONENTS: [
                Button {
                    label = "Click Me"
                    style = "primary"
                    customId = "btn_1"
                }
            ]
        }
        """
        
        result = compile_code(source)
        workflow = result[0]
        
        assert len(workflow["steps"]) == 1
        comp_stmt = workflow["steps"][0]
        assert comp_stmt["type"] == "UI_COMPONENTS"
        assert len(comp_stmt["components"]) == 1
        assert comp_stmt["components"][0]["component_type"] == "Button"
        assert comp_stmt["components"][0]["props"]["label"] == "Click Me"
    
    def test_array_literal(self):
        """Test array literal in parameters"""
        source = """
        WORKFLOW ArrayFlow ON MESSAGE_CREATE {
            ACTION: SEND_MESSAGE options=["Option1", "Option2", "Option3"]
        }
        """
        
        result = compile_code(source)
        workflow = result[0]
        
        action = workflow["steps"][0]
        assert isinstance(action["params"]["options"], list)
        assert len(action["params"]["options"]) == 3
        assert action["params"]["options"][0] == "Option1"
    
    def test_object_literal(self):
        """Test object literal in parameters"""
        source = """
        WORKFLOW ObjFlow ON MESSAGE_CREATE {
            ACTION: SEND_MESSAGE embed={title="Test", color=255}
        }
        """
        
        result = compile_code(source)
        workflow = result[0]
        
        action = workflow["steps"][0]
        assert isinstance(action["params"]["embed"], dict)
        assert action["params"]["embed"]["title"] == "Test"
        assert action["params"]["embed"]["color"] == 255
    
    def test_state_definition(self):
        """Test STATE definition"""
        source = """
        STATE ConfirmationState {
            ACTION: SEND_MESSAGE content="Please confirm"
            COMPONENTS: [
                Button { label="Yes" customId="yes" },
                Button { label="No" customId="no" }
            ]
        }
        """
        
        result = compile_code(source)
        
        assert len(result) == 1
        state = result[0]
        assert state["type"] == "STATE"
        assert state["name"] == "ConfirmationState"
        assert len(state["steps"]) == 2
    
    def test_multiple_definitions(self):
        """Test multiple workflow and state definitions"""
        source = """
        WORKFLOW Flow1 ON EVENT1 {
            ACTION: SEND_MESSAGE content="Flow1"
        }
        
        STATE State1 {
            ACTION: SEND_MESSAGE content="State1"
        }
        
        WORKFLOW Flow2 ON EVENT2 {
            ACTION: SEND_MESSAGE content="Flow2"
        }
        """
        
        result = compile_code(source)
        
        assert len(result) == 3
        assert result[0]["name"] == "Flow1"
        assert result[1]["name"] == "State1"
        assert result[2]["name"] == "Flow2"
    
    def test_complex_workflow(self):
        """Test complex workflow with multiple features"""
        source = """
        WORKFLOW ComplexFlow ON MESSAGE_CREATE WHERE user.verified == TRUE {
            SET message_count = 0
            
            IF message.content contains "help" {
                ACTION: SEND_MESSAGE 
                    channel="support" 
                    content="User needs help"
                    
                COMPONENTS: [
                    Button { label="Assist" customId="assist_btn" }
                ]
                
                ENTER_STATE HelpState
            } ELSE {
                ACTION: REPLY_MESSAGE content="Thank you!"
                SET message_count = 1
            }
        }
        """
        
        result = compile_code(source)
        workflow = result[0]
        
        assert workflow["name"] == "ComplexFlow"
        assert workflow["condition"]["right"] is True
        assert len(workflow["steps"]) == 2  # SET and IF
    
    def test_syntax_error(self):
        """Test that syntax errors are caught"""
        source = """
        WORKFLOW BadFlow ON {
            ACTION SEND_MESSAGE
        }
        """
        
        with pytest.raises(CompilerError):
            compile_code(source)
    
    def test_empty_workflow(self):
        """Test workflow with no statements"""
        source = """
        WORKFLOW EmptyFlow ON SOME_EVENT {
        }
        """
        
        result = compile_code(source)
        workflow = result[0]
        
        assert workflow["name"] == "EmptyFlow"
        assert len(workflow["steps"]) == 0
    
    def test_number_types(self):
        """Test different number formats"""
        source = """
        WORKFLOW NumFlow ON EVENT {
            SET int_val = 42
            SET float_val = 3.14
            SET negative = -10
            SET scientific = 1.5e2
        }
        """
        
        result = compile_code(source)
        workflow = result[0]
        
        assert workflow["steps"][0]["value"] == 42
        assert workflow["steps"][1]["value"] == 3.14
        assert workflow["steps"][2]["value"] == -10
        assert workflow["steps"][3]["value"] == 150.0
    
    def test_boolean_values(self):
        """Test TRUE and FALSE keywords"""
        source = """
        WORKFLOW BoolFlow ON EVENT {
            SET is_active = TRUE
            SET is_disabled = FALSE
        }
        """
        
        result = compile_code(source)
        workflow = result[0]
        
        assert workflow["steps"][0]["value"] is True
        assert workflow["steps"][1]["value"] is False


# Run tests with: pytest test_compiler.py -v
if __name__ == "__main__":
    pytest.main([__file__, "-v"])