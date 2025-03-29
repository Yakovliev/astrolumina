import os
from typing import Dict, Any, List, Optional
from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore_v1.base_query import FieldFilter
from google.api_core.exceptions import AlreadyExists


class FirestoreService:
    def __init__(self):
        project_root = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        self.credentials_path = os.path.join(
            project_root, "firebase-key.json")
        if not os.path.isfile(self.credentials_path):
            raise ValueError(
                f"Firestore credentials file not found at {self.credentials_path}")
        cred = credentials.Certificate(self.credentials_path)
        self.app = initialize_app(cred)
        self.db = firestore.client(self.app)

    def create_document(self, collection: str, document_id: str, data: Dict[str, Any]):
        try:
            self.db.collection(collection).document(document_id).set(data)
        except AlreadyExists as e:
            raise ValueError(
                f"Document already exists: {str(e)} in collection '{collection}'")
        except Exception as e:
            raise ValueError(f"Failed to create document: {str(e)}")

    def get_document(self, collection: str, document_id: str) -> Dict[str, Any]:
        try:
            doc_ref = self.db.collection(collection).document(document_id)
            doc = doc_ref.get()
            if not doc.exists:
                raise ValueError(
                    f"Document {document_id} does not exist in collection '{collection}'")
            return doc.to_dict()
        except Exception as e:
            raise ValueError(f"Failed to retrieve document: {str(e)}")

    def update_document(self, collection: str, document_id: str, data: Dict[str, Any]):
        try:
            doc_ref = self.db.collection(collection).document(document_id)
            if not doc_ref.get().exists:
                raise ValueError(
                    f"Document {document_id} does not exist in collection '{collection}'")
            doc_ref.update(data)
        except Exception as e:
            raise ValueError(f"Failed to update document: {str(e)}")

    def delete_document(self, collection: str, document_id: str) -> bool:
        try:
            doc_ref = self.db.collection(collection).document(document_id)
            if not doc_ref.get().exists:
                raise ValueError(
                    f"Document {document_id} does not exist in collection '{collection}'")
            doc_ref.delete()
            return True
        except Exception as e:
            raise ValueError(f"Failed to delete document: {str(e)}")

    def query_documents(self,
                        collection: str,
                        filters: Optional[List[Dict[str, Any]]] = None,
                        order_by: Optional[str] = None,
                        order_direction: str = 'ASCENDING',
                        limit: Optional[int] = None) -> List[Dict[str, Any]]:
        try:
            query = self.db.collection(collection)

            if filters:
                for filter_dict in filters:
                    field = filter_dict.get('field')
                    op = filter_dict.get('op')
                    value = filter_dict.get('value')

                    if field and op and value is not None:
                        query = query.where(
                            filter=FieldFilter(field, op, value))

            if order_by:
                direction = firestore.Query.DESCENDING if order_direction == 'DESCENDING' else firestore.Query.ASCENDING
                query = query.order_by(order_by, direction=direction)

            if limit:
                query = query.limit(limit)

            docs = query.stream()
            results = []

            for doc in docs:
                doc_dict = doc.to_dict()
                doc_dict['id'] = doc.id
                results.append(doc_dict)

            return results

        except Exception as e:
            raise ValueError(f"Failed to query documents: {str(e)}")

    def batch_create(self, collection: str, items: List[Dict[str, Any]]) -> List[str]:
        try:
            batch = self.db.batch()
            collection_ref = self.db.collection(collection)
            doc_refs = []

            for item in items:
                doc_ref = collection_ref.document()
                doc_refs.append(doc_ref)
                batch.set(doc_ref, item)

            batch.commit()

            return [doc_ref.id for doc_ref in doc_refs]
        except Exception as e:
            raise ValueError(f"Failed to batch create documents: {str(e)}")
