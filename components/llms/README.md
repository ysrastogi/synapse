# LLM Node

## Overview

The LLM (Large Language Model) Node is a flexible and powerful component designed to integrate language models into various workflows. It provides a standardized interface for inputting diverse data types, processing them through a selected language model, and outputting structured results in multiple formats.

## Features

- **Flexible Inputs**: Accepts user messages, tools, and functions as inputs.
- **Configurable Model**: Allows selection of different language models and parameter tuning.
- **Multiple Output Formats**: Supports various output parsing methods for structured data retrieval.
- **Error Handling**: Includes built-in error management and output fixing capabilities.

## Architecture

The LLM Node consists of the following components:

1. **Input Parser**: Standardizes incoming data from various sources.
2. **LLM Processing Core**: Applies the selected model with specified parameters to process inputs.
3. **Output Formatter**: Structures the model's output according to the chosen parsing method.
4. **Error Handler**: Manages exceptions and can attempt to fix incorrect outputs.

## Input Types

- User Message (text)
- Tools (various data structures or functions)
- Functions (callable code snippets)

## Node Properties

- Model Selection (e.g., GPT-3, GPT-4, BERT)
- Model Parameters (e.g., temperature, max_tokens)

## Output Parsers

The node supports multiple output parsing methods, including:

1. OpenAITools
2. OpenAIFunctions
3. JSON
4. XML
5. CSV
6. OutputFixing
7. RetryWithError
8. Pydantic
9. YAML
10. PandasDataFrame
11. Enum
12. Datetime
13. Structured

Each parser is designed to handle specific output formats and data structures.

## Output Types

Depending on the parser used, the node can produce various output types:

- JSON Objects
- Dictionaries
- Lists
- Pydantic Models
- DataFrames
- Enum Values
- Datetime objects
- Structured Dictionaries

# LLM NODE ARCHITECTURE
![LLM NODE](LLM%20Node%20Architecture.svg)