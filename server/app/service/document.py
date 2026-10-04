from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.storage.checksum import calculate_sha256
from app.core.storage.key import document_version_key
from app.core.storage.service import StorageService
from app.models.document import Document, DocumentAccessLevel, DocumentStatus
from app.models.document_version import DocumentVersion
from app.repositories.document_version_repository import DocumentVersionRepository
from app.repositories.document_repository import DocumenetRepository


class DocumentService:
    def __init__(self, db: AsyncSession, storage: StorageService):
        self.db = db
        self.documents = DocumenetRepository(db)
        self.versions = DocumentVersionRepository(db)
        self.storage = storage

    async def create_document(
        self,
        tenant_id: int,
        user_id: int,
        title: str,
        slug: str,
        file_path: str,
        original_filename: str,
        mime_type: str,
        access_level: DocumentAccessLevel,
        description: str | None = None,
        category: str | None = None,
    ) -> Document:
        existing = await self.documents.get_by_slug(slug=slug, tenant_id=tenant_id)

        if existing:
            raise ValueError("A document with this slug already exists")

        document = Document(
            tenant_id=tenant_id,
            title=title,
            slug=slug,
            description=description,
            category=category,
            access_level=access_level,
            status=DocumentStatus.DRAFT,
            created_by=user_id,
            update_by=user_id,
        )

        await self.documents.create(document)

        version = DocumentVersion(
            document_id=self.document.id,
            version_number=1,
            storage_key="pending",
            original_filename=original_filename,
            mime_type=mime_type,
            file_size=Path(file_path).stat().st_size,
            checksum=None,
            uploaded_by=user_id,
        )

        await self.versions.create(version)

        storage_key = document_version_key(
            tenant_id=tenant_id,
            document_id=document.id,
            version_id=document.id,
            filename=original_filename,
        )

        self.storage.upload_file(
            file_path=file_path, object_key=storage_key, content_type=mime_type
        )

        version.storage_key = storage_key
        version.checksum = calculate_sha256(file_path)
        document.current_version_id = version.id

        await self.db.flush()

        await self.db.refresh(document)
        return document
