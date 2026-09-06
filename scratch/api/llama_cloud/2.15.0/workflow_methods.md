# workflow_methods

Source: inspect: llama_cloud.LlamaCloud methods @ 2.15.0
Probed: 2026-08-30

## files.create

### Signature

```
(*, file: 'FileTypes', purpose: 'str', organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, external_file_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'FileCreateResponse'
```

### help()

```
Python Library Documentation: method create in module llama_cloud.resources.files

create(*, file: 'FileTypes', purpose: 'str', organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, external_file_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'FileCreateResponse' method of llama_cloud.resources.files.FilesResource instance
    Upload a file using multipart/form-data.

    Set `purpose` to indicate how the file will be used: `user_data`, `parse`,
    `extract`, `classify`, `split`, `sheet`, or `agent_app`.

    Returns the created file metadata including its ID for use in subsequent parse,
    extract, or classify operations.

    Args:
      file: The file to upload

      purpose: The intended purpose of the file. Valid values: 'user_data', 'parse', 'extract',
          'split', 'classify', 'sheet', 'agent_app'. This determines the storage and
          retention policy for the file.

      external_file_id: The ID of the file in the external system

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds

```

## parsing.parse

### Signature

```
(*, tier: "Union[Literal['fast', 'cost_effective', 'agentic', 'agentic_plus'], str]", version: "Union[Literal['latest', '2026-07-24', '2026-07-23', '2026-07-08', '2026-06-15'], str]", organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, agentic_options: 'Optional[parsing_create_params.AgenticOptions] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, client_name: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, crop_box: 'parsing_create_params.CropBox | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, disable_cache: 'Optional[bool] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, expand: 'SequenceNotStr[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, fast_options: 'Optional[object] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, upload_file: 'Optional[FileTypes] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, file_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, http_proxy: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, input_options: 'parsing_create_params.InputOptions | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, output_options: 'parsing_create_params.OutputOptions | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, page_ranges: 'parsing_create_params.PageRanges | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, processing_control: 'parsing_create_params.ProcessingControl | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, processing_options: 'parsing_create_params.ProcessingOptions | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, source_url: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, webhook_configurations: 'Iterable[parsing_create_params.WebhookConfiguration] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, image_filenames: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, polling_interval: 'float' = 1.0, max_interval: 'float' = 5.0, timeout: 'float' = 7200.0, backoff: 'BackoffStrategy' = 'linear', verbose: 'bool' = False, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None) -> 'ParsingGetResponse'
```

### help()

```
Python Library Documentation: method parse in module llama_cloud.resources.parsing

parse(*, tier: "Union[Literal['fast', 'cost_effective', 'agentic', 'agentic_plus'], str]", version: "Union[Literal['latest', '2026-07-24', '2026-07-23', '2026-07-08', '2026-06-15'], str]", organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, agentic_options: 'Optional[parsing_create_params.AgenticOptions] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, client_name: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, crop_box: 'parsing_create_params.CropBox | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, disable_cache: 'Optional[bool] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, expand: 'SequenceNotStr[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, fast_options: 'Optional[object] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, upload_file: 'Optional[FileTypes] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, file_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, http_proxy: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, input_options: 'parsing_create_params.InputOptions | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, output_options: 'parsing_create_params.OutputOptions | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, page_ranges: 'parsing_create_params.PageRanges | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, processing_control: 'parsing_create_params.ProcessingControl | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, processing_options: 'parsing_create_params.ProcessingOptions | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, source_url: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, webhook_configurations: 'Iterable[parsing_create_params.WebhookConfiguration] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, image_filenames: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, polling_interval: 'float' = 1.0, max_interval: 'float' = 5.0, timeout: 'float' = 7200.0, backoff: 'BackoffStrategy' = 'linear', verbose: 'bool' = False, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None) -> 'ParsingGetResponse' method of llama_cloud.resources.parsing.ParsingResource instance
    Parse a file and wait for it to complete, returning the result.

    This is a convenience method that combines create(), wait_for_completion(),
    and get() into a single call for the most common end-to-end workflow.

    Args:
        tier: The parsing tier to use

        version: Version of the tier configuration

        organization_id: Optional organization ID

        project_id: Optional project ID

        agentic_options: Options for agentic tier parsing (with AI agents).

        client_name: Name of the client making the parsing request

        crop_box: Document crop box boundaries

        disable_cache: Whether to disable caching for this parsing job

        expand: Fields to include: text, markdown, items, text_content_metadata,
          markdown_content_metadata, items_content_metadata, xlsx_content_metadata,
          output_pdf_content_metadata, images_content_metadata. Metadata fields include
          presigned URLs.

        fast_options: Options for fast tier parsing (without AI).

        file: File to upload and parse

        file_id: ID of an existing file in the project to parse

        http_proxy: HTTP proxy URL for network requests (only used with source_url)

        input_options: Input format-specific parsing options

        output_options: Output format and styling options

        page_ranges: Page range selection options

        processing_control: Job processing control and failure handling

        processing_options: Processing options shared across all tiers

        source_url: Source URL to fetch document from

        webhook_configurations: List of webhook configurations for notifications

        image_filenames: Comma-delimited list of image filenames to fetch.

        polling_interval: Initial polling interval in seconds (default: 1.0)

        max_interval: Maximum polling interval for backoff in seconds (default: 5.0)

        timeout: Maximum time to wait in seconds (default: 300.0)

        backoff: Backoff strategy for polling intervals. Options:
            - "constant": Keep the same polling interval
            - "linear": Increase interval by 1 second each poll (default)
            - "exponential": Double the interval each poll

        verbose: Print progress indicators every 10 polls (default: False)

        extra_headers: Send extra headers

        extra_query: Add additional query parameters to the request

        extra_body: Add additional JSON properties to the request

    Returns:
        The parse result (ParsingGetResponse) with job status and optional result data

    Raises:
        PollingTimeoutError: If the job doesn't complete within the timeout period

        PollingError: If the job fails or is cancelled

    Example:
        ```python
        from llama_cloud import LlamaCloud

        client = LlamaCloud(api_key="...")

        # One-shot: parse, wait for completion, and get result
        result = client.parsing.parse(
            tier="fast",
            version="latest",
            source_url="https://example.com/document.pdf",
            expand=["text", "markdown"],
            verbose=True,
        )

        # Result is ready to use immediately
        print(result.text)
        print(result.markdown)
        ```

```

## extract.validate_schema

### Signature

```
(*, data_schema: 'Dict[str, Union[Dict[str, object], Iterable[object], str, float, bool, None]]', extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'ExtractV2SchemaValidateResponse'
```

### help()

```
Python Library Documentation: method validate_schema in module llama_cloud.resources.extract

validate_schema(*, data_schema: 'Dict[str, Union[Dict[str, object], Iterable[object], str, float, bool, None]]', extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'ExtractV2SchemaValidateResponse' method of llama_cloud.resources.extract.ExtractResource instance
    Validate a JSON schema for extraction.

    Args:
      data_schema: JSON Schema to validate for use with extract jobs

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds

```

## extract.run

### Signature

```
(*, file_input: 'str', organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, configuration: 'Optional[ExtractConfigurationParam] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, configuration_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, webhook_configurations: 'Optional[Iterable[extract_create_params.WebhookConfiguration]] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, polling_interval: 'float' = 1.0, max_interval: 'float' = 5.0, polling_timeout: 'float' = 7200.0, backoff: 'BackoffStrategy' = 'linear', verbose: 'bool' = False, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'ExtractV2Job'
```

### help()

```
Python Library Documentation: method run in module llama_cloud.resources.extract

run(*, file_input: 'str', organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, configuration: 'Optional[ExtractConfigurationParam] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, configuration_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, webhook_configurations: 'Optional[Iterable[extract_create_params.WebhookConfiguration]] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, polling_interval: 'float' = 1.0, max_interval: 'float' = 5.0, polling_timeout: 'float' = 7200.0, backoff: 'BackoffStrategy' = 'linear', verbose: 'bool' = False, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'ExtractV2Job' method of llama_cloud.resources.extract.ExtractResource instance
    Create an extraction job, wait for it to complete, and return the result.

    This is a convenience method that combines create() and wait_for_completion()
    into a single call for the most common end-to-end workflow.

    Args:
        file_input: File ID or parse job ID to extract from.

        configuration: Inline extraction configuration with schema and options.

        configuration_id: Saved extract configuration ID (mutually exclusive with configuration).

        webhook_configurations: The outbound webhook configurations.

        polling_interval: Initial polling interval in seconds (default: 1.0).

        max_interval: Maximum polling interval for backoff in seconds (default: 5.0).

        polling_timeout: Maximum time to wait in seconds (default: 2 hours).

        backoff: Backoff strategy: "constant", "linear" (default), or "exponential".

        verbose: Print progress indicators every 10 polls (default: False).

    Example:
        ```python
        result = client.extract.run(
            file_input="dfl-aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            configuration={"data_schema": {...}, "extraction_target": "per_doc"},
            verbose=True,
        )
        print(result.extract_result)
        ```

```

## beta.directories.create

### Signature

```
(*, name: 'str', organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, connector_subscription_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, description: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, system_metadata: 'Optional[Dict[str, object]] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, type: "Literal['ephemeral', 'user'] | Omit" = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'DirectoryCreateResponse'
```

### help()

```
Python Library Documentation: method create in module llama_cloud.resources.beta.directories.directories

create(*, name: 'str', organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, connector_subscription_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, description: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, system_metadata: 'Optional[Dict[str, object]] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, type: "Literal['ephemeral', 'user'] | Omit" = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'DirectoryCreateResponse' method of llama_cloud.resources.beta.directories.directories.DirectoriesResource instance
    Create a new directory within the specified project.

    Args:
      name: Human-readable name for the directory.

      connector_subscription_id: Connector Subscription whose files sync into this directory. Omit for manual
          uploads.

      description: Optional description shown to users.

      system_metadata: Reserved system-managed metadata.

      type: Directory type. Use 'ephemeral' for batch processing with automatic cleanup.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds

```

## beta.directories.files.add

### Signature

```
(directory_id: 'str', *, file_id: 'str', organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, display_name: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, metadata: 'Optional[Dict[str, Union[str, int, float, bool, None, SequenceNotStr[str]]]] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, unique_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'FileAddResponse'
```

### help()

```
Python Library Documentation: method add in module llama_cloud.resources.beta.directories.files

add(directory_id: 'str', *, file_id: 'str', organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, display_name: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, metadata: 'Optional[Dict[str, Union[str, int, float, bool, None, SequenceNotStr[str]]]] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, unique_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'FileAddResponse' method of llama_cloud.resources.beta.directories.files.FilesResource instance
    Create a new file within the specified directory; the directory must exist in
    the project and `file_id` must reference an existing file.

    Args:
      file_id: File ID for the storage location (required).

      display_name: Display name for the file. If not provided, will use the file's name.

      metadata: User-defined metadata key-value pairs to associate with the file.

      unique_id: Unique identifier for the file in the directory. If not provided, will use the
          file's external_file_id or name.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds

```

## beta.indexes.list

### Signature

```
(*, organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, page_size: 'Optional[int] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, page_token: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, source_directory_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'SyncPaginatedCursor[IndexListResponse]'
```

### help()

```
Python Library Documentation: method list in module llama_cloud.resources.beta.indexes

list(*, organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, page_size: 'Optional[int] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, page_token: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, source_directory_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'SyncPaginatedCursor[IndexListResponse]' method of llama_cloud.resources.beta.indexes.IndexesResource instance
    List indexes for the current project.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds

```

## beta.indexes.create

### Signature

```
(*, source_directory_id: 'str', organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, description: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, name: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, products: 'Optional[Iterable[index_create_params.Product]] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, store_attachments: 'Optional[SequenceNotStr[str]] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, sync_frequency: 'str | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, vector_target: "Literal['DEFAULT', 'DISABLED'] | Omit" = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'IndexCreateResponse'
```

### help()

```
Python Library Documentation: method create in module llama_cloud.resources.beta.indexes

create(*, source_directory_id: 'str', organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, description: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, name: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, products: 'Optional[Iterable[index_create_params.Product]] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, store_attachments: 'Optional[SequenceNotStr[str]] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, sync_frequency: 'str | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, vector_target: "Literal['DEFAULT', 'DISABLED'] | Omit" = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'IndexCreateResponse' method of llama_cloud.resources.beta.indexes.IndexesResource instance
    Create a searchable index over a source directory.

    Args:
      source_directory_id: ID of the source directory containing your documents.

      description: Optional description of the index.

      name: Optional display name for the index. If omitted, the index is named after the
          source directory.

      products: Product configurations for syncing. Omit to use a default parse configuration.
          Include an explicit entry per product type (e.g. parse, extract) to override the
          default.

      store_attachments:
          Attachment kinds to store alongside parsed output. Each entry must be one of:
          screenshots, items. For example, ['screenshots'] renders and stores per-page
          screenshots; ['items'] stores structured items with bounding boxes. Omit or pass
          an empty list to skip attachments.

      sync_frequency: How often to re-run the sync. One of: manual, daily, on_source_change. Defaults
          to manual.

      vector_target: Vector export destination for the index. 'DEFAULT' exports to the managed vector
          DB destination resolved from configuration. 'DISABLED' skips vector export — the
          export destination falls back to 'Download'.

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds

```

## beta.indexes.get

### Signature

```
(index_id: 'str', *, organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'IndexGetResponse'
```

### help()

```
Python Library Documentation: method get in module llama_cloud.resources.beta.indexes

get(index_id: 'str', *, organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'IndexGetResponse' method of llama_cloud.resources.beta.indexes.IndexesResource instance
    Get an index by ID.

    Args:
      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds

```

## beta.retrieval.retrieve

### Signature

```
(*, index_id: 'str', query: 'str', organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, custom_filters: 'Optional[Dict[str, Optional[retrieval_retrieve_params.CustomFilters]]] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, full_text_pipeline_weight: 'Optional[float] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, num_candidates: 'Optional[int] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, rerank: 'retrieval_retrieve_params.Rerank | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, score_threshold: 'Optional[float] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, static_filters: 'Optional[retrieval_retrieve_params.StaticFilters] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, top_k: 'Optional[int] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, vector_pipeline_weight: 'Optional[float] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'RetrievalRetrieveResponse'
```

### help()

```
Python Library Documentation: method retrieve in module llama_cloud.resources.beta.retrieval

retrieve(*, index_id: 'str', query: 'str', organization_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, project_id: 'Optional[str] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, custom_filters: 'Optional[Dict[str, Optional[retrieval_retrieve_params.CustomFilters]]] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, full_text_pipeline_weight: 'Optional[float] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, num_candidates: 'Optional[int] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, rerank: 'retrieval_retrieve_params.Rerank | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, score_threshold: 'Optional[float] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, static_filters: 'Optional[retrieval_retrieve_params.StaticFilters] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, top_k: 'Optional[int] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, vector_pipeline_weight: 'Optional[float] | Omit' = <llama_cloud.Omit object at 0x7f68cd645b50>, extra_headers: 'Headers | None' = None, extra_query: 'Query | None' = None, extra_body: 'Body | None' = None, timeout: 'float | httpx.Timeout | None | NotGiven' = NOT_GIVEN) -> 'RetrievalRetrieveResponse' method of llama_cloud.resources.beta.retrieval.RetrievalResource instance
    Retrieve relevant chunks via hybrid search (vector + full-text), with filtering
    on built-in or user-defined metadata.

    Args:
      index_id: ID of the index to retrieve against.

      query: Natural-language query to retrieve relevant chunks.

      custom_filters: Filters on user-defined metadata fields.

      full_text_pipeline_weight: Weight of the full-text search pipeline (0-1).

      num_candidates: Number of candidates for approximate nearest neighbor search.

      rerank: Reranking configuration applied after hybrid search. Enabled by default.

      score_threshold: Minimum score threshold for returned results.

      static_filters: Filters on built-in document fields (page range, chunk index, etc.).

      top_k: Maximum number of results to return.

      vector_pipeline_weight: Weight of the vector search pipeline (0-1).

      extra_headers: Send extra headers

      extra_query: Add additional query parameters to the request

      extra_body: Add additional JSON properties to the request

      timeout: Override the client-level default timeout for this request, in seconds

```

## Usage (agent synthesis)

- **Call:** Upload with `files.create`, then use the synchronous Parse, Extract, or Index workflow methods shown above.
- **Don't call:** Do not use older `llama_cloud_services` helpers or TypeScript camelCase method names.
- **Trap:** Parse uses `timeout`; Extract uses `polling_timeout`. Expanded parse content and presigned artifacts must be requested explicitly.
- **Returns:** Pydantic response models. Serialize them with `model_dump(mode="json")` before writing JSON.
