import { Button } from "@/components/ui/button";
import { Book, Check, Copy, Library, Search, SearchX, Zap } from "lucide-react";
import { useMemo, useState } from "react";
import { categoryInfo, syntaxExamples } from "../data/syntaxData";
import type { SyntaxCategory, SyntaxExample } from "../documentation.d";
import { useClipboard } from "../hooks/useClipboard";
import "./DocumentationPage.css";

const QUICK_REFS = [
  "WORKFLOW",
  "ON",
  "WHERE",
  "ACTION:",
  "IF",
  "ELSE",
  "STATE",
  "ENTER_STATE",
  "SET",
  "EXTRACT",
  "COMPONENTS:",
];

export default function DocumentationPage() {
  const [selectedCategory, setSelectedCategory] = useState<SyntaxCategory | "all">("all");
  const [searchQuery, setSearchQuery] = useState("");
  const { copiedId, copyToClipboard } = useClipboard();

  const categories = Object.entries(categoryInfo) as [SyntaxCategory, typeof categoryInfo[SyntaxCategory]][];

  const filteredExamples = useMemo(() => {
    let examples = syntaxExamples;

    // Filter by category
    if (selectedCategory !== "all") {
      examples = examples.filter((ex) => ex.category === selectedCategory);
    }

    // Filter by search
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      examples = examples.filter(
        (ex) =>
          ex.title.toLowerCase().includes(query) ||
          ex.description.toLowerCase().includes(query) ||
          ex.code.toLowerCase().includes(query)
      );
    }

    return examples;
  }, [selectedCategory, searchQuery]);

  const getCategoryCount = (category: SyntaxCategory) =>
    syntaxExamples.filter((ex) => ex.category === category).length;

  const handleQuickRefClick = (keyword: string) => {
    setSearchQuery(keyword);
    setSelectedCategory("all");
  };

  return (
    <div className="documentation-container">
      {/* Header */}
      <div className="documentation-header">
        <h1>
          <Book className="size-7 text-primary" />
          GuildFlow DSL Documentation
        </h1>
        <p>
          Learn the GuildFlow Domain-Specific Language for creating Discord bot workflows.
          Click any code snippet to copy it to your clipboard.
        </p>
      </div>

      <div className="documentation-content">
        {/* Sidebar */}
        <div className="documentation-sidebar">
          {/* Search */}
          <div className="search-container">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search examples..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-input pl-10"
              />
            </div>
          </div>

          {/* Categories */}
          <div className="category-list">
            <div
              className={`category-item ${selectedCategory === "all" ? "active" : ""}`}
              onClick={() => setSelectedCategory("all")}
            >
              <Library className="category-icon size-5" />
              <div className="category-info">
                <span className="category-name">All Examples</span>
                <span className="category-count">{syntaxExamples.length} examples</span>
              </div>
            </div>

            {categories.map(([key, info]) => (
              <div
                key={key}
                className={`category-item ${selectedCategory === key ? "active" : ""}`}
                onClick={() => setSelectedCategory(key)}
              >
                <info.Icon className="category-icon size-5" />
                <div className="category-info">
                  <span className="category-name">{info.name}</span>
                  <span className="category-count">{getCategoryCount(key)} examples</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="documentation-main">
          {/* Quick Reference */}
          <div className="quick-reference">
            <h3>
              <Zap className="size-4" />
              Quick Reference - Keywords
            </h3>
            <div className="quick-ref-items">
              {QUICK_REFS.map((keyword) => (
                <span
                  key={keyword}
                  className="quick-ref-tag"
                  onClick={() => handleQuickRefClick(keyword)}
                >
                  {keyword}
                </span>
              ))}
            </div>
          </div>

          {/* Category Header */}
          {selectedCategory !== "all" && categoryInfo[selectedCategory] && (
            <div className="category-header">
              <h2>
                {(() => {
                  const CategoryIcon = categoryInfo[selectedCategory].Icon;
                  return <CategoryIcon className="size-6" />;
                })()}
                {categoryInfo[selectedCategory].name}
              </h2>
              <p>{categoryInfo[selectedCategory].description}</p>
            </div>
          )}

          {/* Examples */}
          {filteredExamples.length > 0 ? (
            <div className="examples-grid">
              {filteredExamples.map((example) => (
                <CodeCard
                  key={example.id}
                  example={example}
                  isCopied={copiedId === example.id}
                  onCopy={() => copyToClipboard(example.code, example.id)}
                />
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <SearchX className="empty-state-icon size-12 mx-auto" />
              <h3>No examples found</h3>
              <p>Try adjusting your search or selecting a different category.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

interface CodeCardProps {
  example: SyntaxExample;
  isCopied: boolean;
  onCopy: () => void;
}

function CodeCard({ example, isCopied, onCopy }: CodeCardProps) {
  const categoryData = categoryInfo[example.category];
  const CategoryIcon = categoryData?.Icon;

  return (
    <div className="code-card">
      <div className="code-card-header">
        <div>
          <div className="code-card-title">
            {CategoryIcon && <CategoryIcon className="size-4 inline mr-2" />}
            {example.title}
          </div>
          <div className="code-card-description">{example.description}</div>
        </div>
        <div className="code-card-actions">
          <Button
            size="sm"
            variant={isCopied ? "default" : "outline"}
            className={`copy-btn ${isCopied ? "copied" : ""}`}
            onClick={onCopy}
          >
            {isCopied ? (
              <>
                <Check className="size-3" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="size-3" />
                Copy
              </>
            )}
          </Button>
        </div>
      </div>
      <div className="code-card-content">
        <pre className="code-block">{example.code}</pre>
      </div>
    </div>
  );
}
