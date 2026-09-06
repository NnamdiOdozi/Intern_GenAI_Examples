# LlamaCloud response models (2.15.0)

## parse_response

```
llama_cloud.types.parsing_get_response.ParsingGetResponse
  job: <class 'llama_cloud.types.parsing_get_response.Job'>
    llama_cloud.types.parsing_get_response.Job
      id: <class 'str'>
      project_id: <class 'str'>
      status: typing.Literal['CANCELLED', 'COMPLETED', 'FAILED', 'PENDING', 'RUNNING']
      created_at: typing.Optional[datetime.datetime]
      error_message: typing.Optional[str]
      name: typing.Optional[str]
      tier: typing.Optional[str]
      updated_at: typing.Optional[datetime.datetime]
      usage: typing.Optional[llama_cloud.types.parsing_get_response.JobUsage]
        llama_cloud.types.parsing_get_response.JobUsage
      user_metadata: typing.Optional[typing.Dict[str, str]]
  forms: typing.Optional[llama_cloud.types.parsing_get_response.Forms]
    llama_cloud.types.parsing_get_response.Forms
      pages: typing.List[typing.Union[llama_cloud.types.parsing_get_response.FormsPageFormsResultPage, llama_cloud.types.parsing_get_response.FormsPageFailedFormsPage]]
  images_content_metadata: typing.Optional[llama_cloud.types.parsing_get_response.ImagesContentMetadata]
    llama_cloud.types.parsing_get_response.ImagesContentMetadata
      images: typing.List[llama_cloud.types.parsing_get_response.ImagesContentMetadataImage]
        llama_cloud.types.parsing_get_response.ImagesContentMetadataImage
      total_count: <class 'int'>
  items: typing.Optional[llama_cloud.types.parsing_get_response.Items]
    llama_cloud.types.parsing_get_response.Items
      pages: typing.List[typing.Union[llama_cloud.types.parsing_get_response.ItemsPageStructuredResultPage, llama_cloud.types.parsing_get_response.ItemsPageFailedStructuredPage]]
  job_metadata: typing.Optional[typing.Dict[str, object]]
  markdown: typing.Optional[llama_cloud.types.parsing_get_response.Markdown]
    llama_cloud.types.parsing_get_response.Markdown
      pages: typing.List[typing.Union[llama_cloud.types.parsing_get_response.MarkdownPageMarkdownResultPage, llama_cloud.types.parsing_get_response.MarkdownPageFailedMarkdownPage]]
  markdown_full: typing.Optional[str]
  metadata: typing.Optional[llama_cloud.types.parsing_get_response.Metadata]
    llama_cloud.types.parsing_get_response.Metadata
      pages: typing.List[llama_cloud.types.parsing_get_response.MetadataPage]
        llama_cloud.types.parsing_get_response.MetadataPage
      document: typing.Optional[llama_cloud.types.parsing_get_response.MetadataDocument]
        llama_cloud.types.parsing_get_response.MetadataDocument
  raw_parameters: typing.Optional[typing.Dict[str, object]]
  result_content_metadata: typing.Optional[typing.Dict[str, llama_cloud.types.parsing_get_response.ResultContentMetadata]]
  text: typing.Optional[llama_cloud.types.parsing_get_response.Text]
    llama_cloud.types.parsing_get_response.Text
      pages: typing.List[llama_cloud.types.parsing_get_response.TextPage]
        llama_cloud.types.parsing_get_response.TextPage
  text_full: typing.Optional[str]
```

## extract_response

```
llama_cloud.types.extract_v2_job.ExtractV2Job
  id: <class 'str'>
  created_at: <class 'datetime.datetime'>
  file_input: <class 'str'>
  project_id: <class 'str'>
  status: <class 'str'>
  updated_at: <class 'datetime.datetime'>
  configuration: typing.Optional[llama_cloud.types.extract_configuration.ExtractConfiguration]
    llama_cloud.types.extract_configuration.ExtractConfiguration
      data_schema: typing.Dict[str, typing.Union[typing.Dict[str, object], typing.List[object], str, float, bool, NoneType]]
      cite_sources: typing.Optional[bool]
      confidence_scores: typing.Optional[bool]
      disable_cache: typing.Optional[bool]
      extraction_target: typing.Optional[typing.Literal['per_doc', 'per_page', 'per_table_row']]
      max_pages: typing.Optional[int]
      parse_config_id: typing.Optional[str]
      parse_tier: typing.Optional[str]
      sheet_names: typing.Optional[typing.List[str]]
      spreadsheet_mode: typing.Optional[bool]
      system_prompt: typing.Optional[str]
      target_pages: typing.Optional[str]
      tier: typing.Optional[typing.Literal['agentic', 'agentic_plus', 'cost_effective', 'turbo']]
      version: typing.Optional[str]
  configuration_id: typing.Optional[str]
  error_message: typing.Optional[str]
  extract_metadata: typing.Optional[llama_cloud.types.extract_job_metadata.ExtractJobMetadata]
    llama_cloud.types.extract_job_metadata.ExtractJobMetadata
      field_metadata: typing.Optional[llama_cloud.types.extracted_field_metadata.ExtractedFieldMetadata]
        llama_cloud.types.extracted_field_metadata.ExtractedFieldMetadata
      parse_job_id: typing.Optional[str]
      parse_tier: typing.Optional[str]
  extract_result: typing.Union[typing.Dict[str, typing.Union[typing.Dict[str, object], typing.List[object], str, float, bool, NoneType]], typing.List[typing.Dict[str, typing.Union[typing.Dict[str, object], typing.List[object], str, float, bool, NoneType]]], NoneType]
  metadata: typing.Optional[llama_cloud.types.extract_v2_job.Metadata]
    llama_cloud.types.extract_v2_job.Metadata
      usage: typing.Optional[llama_cloud.types.extract_job_usage.ExtractJobUsage]
        llama_cloud.types.extract_job_usage.ExtractJobUsage
  usage: typing.Optional[llama_cloud.types.extract_v2_job.Usage]
    llama_cloud.types.extract_v2_job.Usage
      credits: typing.Optional[float]
      extract_credits: typing.Optional[float]
      parse_credits: typing.Optional[float]
```

## index_response

```
llama_cloud.types.beta.index_get_response.IndexGetResponse
  id: <class 'str'>
  export_config_id: <class 'str'>
  name: <class 'str'>
  output_directory_id: <class 'str'>
  project_id: <class 'str'>
  source_directory_id: <class 'str'>
  sync_config_id: <class 'str'>
  created_at: typing.Optional[datetime.datetime]
  description: typing.Optional[str]
  last_exported_at: typing.Optional[datetime.datetime]
  last_synced_at: typing.Optional[datetime.datetime]
  metadata: typing.Optional[typing.Dict[str, object]]
  updated_at: typing.Optional[datetime.datetime]
```

## retrieval_response

```
llama_cloud.types.beta.retrieval_retrieve_response.RetrievalRetrieveResponse
  results: typing.List[llama_cloud.types.beta.retrieval_retrieve_response.Result]
    llama_cloud.types.beta.retrieval_retrieve_response.Result
      content: <class 'str'>
      metadata: typing.Optional[typing.Dict[str, typing.Union[str, int, float, bool, NoneType, typing.List[str]]]]
      rerank_score: typing.Optional[float]
      score: typing.Optional[float]
      static_fields: typing.Optional[llama_cloud.types.beta.retrieval_retrieve_response.ResultStaticFields]
        llama_cloud.types.beta.retrieval_retrieve_response.ResultStaticFields
```

## MarkdownPageMarkdownResultPage

```
llama_cloud.types.parsing_get_response.MarkdownPageMarkdownResultPage
  markdown: <class 'str'>
  page_number: <class 'int'>
  success: typing.Literal[True]
  footer: typing.Optional[str]
  header: typing.Optional[str]
  line_numbers: typing.Optional[typing.List[llama_cloud.types.parsing_get_response.MarkdownPageMarkdownResultPageLineNumber]]
```

## MarkdownPageFailedMarkdownPage

```
llama_cloud.types.parsing_get_response.MarkdownPageFailedMarkdownPage
  error: <class 'str'>
  page_number: <class 'int'>
  success: typing.Literal[False]
```

## ResultContentMetadata

```
llama_cloud.types.parsing_get_response.ResultContentMetadata
  size_bytes: <class 'int'>
  exists: typing.Optional[bool]
  presigned_url: typing.Optional[str]
```

## ResultStaticFields

```
llama_cloud.types.beta.retrieval_retrieve_response.ResultStaticFields
  attachments: typing.Optional[typing.List[llama_cloud.types.beta.retrieval_retrieve_response.ResultStaticFieldsAttachment]]
  chunk_end_char: typing.Optional[int]
  chunk_index: typing.Optional[int]
  chunk_start_char: typing.Optional[int]
  chunk_token_count: typing.Optional[int]
  page_range_end: typing.Optional[int]
  page_range_start: typing.Optional[int]
  parsed_directory_file_id: typing.Optional[str]
```
