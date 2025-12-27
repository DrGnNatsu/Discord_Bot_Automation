import {
    BarChart3,
    Box,
    GitBranch,
    LayoutGrid,
    Target,
    Zap,
} from "lucide-react";
import type { CategoryInfo, SyntaxCategory, SyntaxExample } from "../documentation.d";

export const categoryInfo: Record<SyntaxCategory, CategoryInfo> = {
  workflow: {
    name: "Workflow Definition",
    description: "Define automated workflows that trigger on Discord events",
    Icon: Zap,
  },
  action: {
    name: "Actions",
    description: "Execute commands like sending messages, banning users, or adding roles",
    Icon: Target,
  },
  logic: {
    name: "Logic & Conditions",
    description: "Add conditional logic to control workflow execution",
    Icon: GitBranch,
  },
  state: {
    name: "State Management",
    description: "Define and transition between conversation states",
    Icon: BarChart3,
  },
  component: {
    name: "UI Components",
    description: "Add interactive components like buttons and select menus",
    Icon: LayoutGrid,
  },
  variable: {
    name: "Variables & Data",
    description: "Set and extract variables for data manipulation",
    Icon: Box,
  },
};

export const syntaxExamples: SyntaxExample[] = [
  // ===== WORKFLOW EXAMPLES =====
  {
    id: "workflow-basic",
    title: "Basic Workflow",
    description: "A simple workflow that triggers on a message event",
    code: `WORKFLOW welcome_bot ON message {
    ACTION: SEND_MESSAGE channel="general" content="Hello!"
}`,
    category: "workflow",
  },
  {
    id: "workflow-with-filter",
    title: "Workflow with Filter",
    description: "Trigger only when a specific condition is met using WHERE clause",
    code: `WORKFLOW anti_spam ON message WHERE message.content contains "spam" {
    ACTION: TIMEOUT_USER duration=300
    ACTION: REPLY_MESSAGE content="You have been timed out for spam."
}`,
    category: "workflow",
  },
  {
    id: "workflow-member-join",
    title: "Member Join Event",
    description: "Welcome new members when they join the server",
    code: `WORKFLOW greet_new_members ON member_join {
    ACTION: SEND_MESSAGE channel="welcome" content="Welcome to the server!"
    ACTION: ADD_ROLE role="Member"
}`,
    category: "workflow",
  },

  // ===== ACTION EXAMPLES =====
  {
    id: "action-send-message",
    title: "Send Message",
    description: "Send a message to a specific channel",
    code: `ACTION: SEND_MESSAGE channel="announcements" content="Important update!"`,
    category: "action",
  },
  {
    id: "action-reply-message",
    title: "Reply to Message",
    description: "Reply directly to the triggering message",
    code: `ACTION: REPLY_MESSAGE content="Thanks for your message!"`,
    category: "action",
  },
  {
    id: "action-ban-user",
    title: "Ban User",
    description: "Ban a user from the server",
    code: `ACTION: BAN_USER reason="Violating server rules"`,
    category: "action",
  },
  {
    id: "action-timeout-user",
    title: "Timeout User",
    description: "Temporarily mute a user for a specified duration (in seconds)",
    code: `ACTION: TIMEOUT_USER duration=600`,
    category: "action",
  },
  {
    id: "action-add-role",
    title: "Add Role",
    description: "Add a role to the user who triggered the event",
    code: `ACTION: ADD_ROLE role="Verified"`,
    category: "action",
  },

  // ===== LOGIC EXAMPLES =====
  {
    id: "logic-if-basic",
    title: "Basic IF Statement",
    description: "Execute actions conditionally based on a comparison",
    code: `IF user.strikes > 3 {
    ACTION: BAN_USER reason="Too many strikes"
}`,
    category: "logic",
  },
  {
    id: "logic-if-else",
    title: "IF-ELSE Statement",
    description: "Execute different actions based on a condition",
    code: `IF user.level > 10 {
    ACTION: ADD_ROLE role="Veteran"
} ELSE {
    ACTION: REPLY_MESSAGE content="Keep participating to level up!"
}`,
    category: "logic",
  },
  {
    id: "logic-contains",
    title: "Contains Check",
    description: "Check if a value contains a specific string",
    code: `IF message.content contains "discord.gg" {
    ACTION: TIMEOUT_USER duration=300
    ACTION: REPLY_MESSAGE content="No invite links allowed!"
}`,
    category: "logic",
  },
  {
    id: "logic-equality",
    title: "Equality Comparisons",
    description: "Compare values using == and !=",
    code: `IF user.role == "Admin" {
    ACTION: REPLY_MESSAGE content="Hello Admin!"
}

IF user.status != "verified" {
    ACTION: REPLY_MESSAGE content="Please verify your account."
}`,
    category: "logic",
  },

  // ===== STATE EXAMPLES =====
  {
    id: "state-definition",
    title: "State Definition",
    description: "Define a conversation state with its own logic",
    code: `STATE awaiting_confirmation {
    IF user.response == "yes" {
        ACTION: REPLY_MESSAGE content="Confirmed!"
        ENTER_STATE completed
    } ELSE {
        ACTION: REPLY_MESSAGE content="Cancelled."
        ENTER_STATE idle
    }
}`,
    category: "state",
  },
  {
    id: "state-transition",
    title: "State Transition",
    description: "Move to a different state",
    code: `ENTER_STATE awaiting_confirmation`,
    category: "state",
  },

  // ===== COMPONENT EXAMPLES =====
  {
    id: "component-button",
    title: "Button Component",
    description: "Add interactive buttons to messages",
    code: `COMPONENTS: [
    Button {
        label = "Click Me"
        style = "primary"
        action = "handle_click"
    },
    Button {
        label = "Cancel"
        style = "danger"
        action = "handle_cancel"
    }
]`,
    category: "component",
  },
  {
    id: "component-select-menu",
    title: "Select Menu",
    description: "Add a dropdown selection menu",
    code: `COMPONENTS: [
    SelectMenu {
        placeholder = "Choose an option"
        options = [
            { label = "Option 1", value = "opt1" },
            { label = "Option 2", value = "opt2" }
        ]
    }
]`,
    category: "component",
  },

  // ===== VARIABLE EXAMPLES =====
  {
    id: "variable-set",
    title: "Set Variable",
    description: "Assign a value to a variable",
    code: `SET user.warning_count = 1
SET server.welcome_message = "Welcome to our server!"`,
    category: "variable",
  },
  {
    id: "variable-extract",
    title: "Extract Field",
    description: "Extract a field from an object into a variable",
    code: `EXTRACT FIELD message.author AS sender_name`,
    category: "variable",
  },

  // ===== COMPLETE EXAMPLES =====
  {
    id: "complete-moderation",
    title: "Complete: Moderation Bot",
    description: "A complete moderation workflow with multiple actions",
    code: `WORKFLOW moderation_bot ON message WHERE message.content contains "badword" {
    SET user.strikes = user.strikes + 1
    
    IF user.strikes > 3 {
        ACTION: BAN_USER reason="Exceeded strike limit"
        ACTION: SEND_MESSAGE channel="mod-log" content="User banned for violations"
    } ELSE {
        ACTION: TIMEOUT_USER duration=300
        ACTION: REPLY_MESSAGE content="Warning! Watch your language."
    }
}`,
    category: "workflow",
  },
  {
    id: "complete-verification",
    title: "Complete: Verification System",
    description: "A verification workflow with button interaction",
    code: `WORKFLOW verify_user ON button_click WHERE button.id == "verify_btn" {
    ACTION: ADD_ROLE role="Verified"
    ACTION: REPLY_MESSAGE content="You have been verified!"
    ACTION: SEND_MESSAGE channel="welcome" content="A new member has been verified!"
}`,
    category: "workflow",
  },
  {
    id: "golden-path-test",
    title: "🧪 Golden Path Test",
    description: "Use this to test the complete system integration",
    code: `WORKFLOW final_check ON message {
    ACTION: REPLY_MESSAGE content="System Operational"
}`,
    category: "workflow",
  },
];
