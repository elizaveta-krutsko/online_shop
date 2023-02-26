from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sql_online_shop import crud, schemas
from dependencies import get_db
from sqlalchemy import exc

router = APIRouter(
    prefix="/api/v1/categories",
    tags=["categories"],
)


@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_category(db=db, category=category)
    except exc.IntegrityError as err:
        err_msg = str(err.orig).split(':')[-1].replace('\n', '').strip()
        raise HTTPException(status_code=400, detail=err_msg)


@router.get("/", response_model=list[schemas.Category])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    copied_categories = list([i.__dict__ for i in categories])

    # TODO: Move createTree function into some utils file and import here
    def createTree(nodes=[], parent_id=None, config={}):
        '''
            nodes       - List of flat nodes to be converted into the tree
            parentId    - Parent node id to collect children
            config      - Dict with the keys to dynamically construct the tree
        '''
        return list([{**i, config["children_path"]: createTree(nodes, i[config["key"]], config)} for i in nodes if
                     i[config["parentKey"]] == parent_id])
    return createTree(copied_categories, None, {"key": "id", "parentKey": "parent_category_id", "children_path": "child_categories"})


@router.get("/{category_id}", response_model=schemas.Category)
def get_category_child_list(category_id: int, db: Session = Depends(get_db)):
    if not (db_category := crud.get_category_child_list(db, category_id=category_id)):
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        db_category = crud.delete_category(db, category_id=category_id)
    except exc.IntegrityError as err:
        err_msg = str(err.orig).split(':')[-1].replace('\n', '').strip()
        raise HTTPException(status_code=400, detail=err_msg)

    if db_category:
        return f'Row with id = {category_id} was successfully deleted'
    else:
        raise HTTPException(status_code=404, detail="Record not found")


@router.patch("/{category_id}")
def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    if crud.update_category(db, category_id=category_id, category=category):
        return f'Row with id = {category_id} was successfully updated'
    else:
        raise HTTPException(status_code=404, detail="Category not found")
