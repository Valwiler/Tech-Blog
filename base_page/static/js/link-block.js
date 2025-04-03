class LinkBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );

        const getAncestors = (div, selector) => {
            let divParentElement = div;
            let ancestorBlock = null;
            while (divParentElement) {
                divParentElement = divParentElement.parentElement;
                if (divParentElement && divParentElement.getAttribute("data-contentpath") === selector) {
                    ancestorBlock = divParentElement;
                    return ancestorBlock;
                }
            }
            if (!divParentElement) {
                console.log('Reached an element with no parent.');
            }
        }

        const testVisibility = () => {
            block.childBlocks.content_type.widget.input.onchange = null;
            block.childBlocks.link_url.widget.input.onchange = null;
            block.childBlocks.link_page.widget.input.onchange = null;

            let chosenLinkType = block.childBlocks.content_type.widget.input.value;
            if (chosenLinkType === 'l') {
                urlParent.style.display = "block";
                pageParent.style.display = "block";
                block.childBlocks.document.widget.clear();
                block.childBlocks.link_page.widget.chooserElement.className;
                documentParent.style.display = "None";
                if (block.childBlocks.link_page.widget.chooserElement.className != "chooser page-chooser blank") {
                    // If a page is chosen via chooser, hide the url field
                    urlParent.style.display = "None";
                }
                else {
                    // if no page is chosen, show the url field
                    urlParent.style.display = "block";
                }

                if (block.childBlocks.link_url.widget.input.value != "") {
                    // if the url has some value in it, empty the chosen page and hide the page field
                    block.childBlocks.link_page.widget.clear();
                    pageParent.style.display = "None";
                }
                else {
                    // if the url is empty, show the page field
                    pageParent.style.display = "block";
                }
            }
            else if (chosenLinkType === 'd') {
                // if the link type is a document, hide both the page and url field and empty their values
                // also displays the document field
                documentParent.style.display = "block";
                urlParent.style.display = "None";
                pageParent.style.display = "None";
                block.childBlocks.link_page.widget.clear();
                block.childBlocks.link_url.widget.input.value = "";
            }
            else {
                urlParent.style.display = "None";
                pageParent.style.display = "None";
                documentParent.style.display = "None";
                block.childBlocks.link_page.widget.clear();
                block.childBlocks.document.widget.clear() ;
                block.childBlocks.link_url.widget.input.value = "";
            }
            block.childBlocks.content_type.widget.input.onchange = testVisibility;
            block.childBlocks.link_url.widget.input.onchange = testVisibility;
            block.childBlocks.link_page.widget.input.onchange = testVisibility;
        }

        const urlParent = getAncestors(block.childBlocks.link_url.element, "link_url");
        const pageParent = getAncestors(block.childBlocks.link_page.element, "link_page");
        const documentParent = getAncestors(block.childBlocks.document.element, "document");

        block.childBlocks.content_type.widget.input.onchange = testVisibility;
        block.childBlocks.link_url.widget.input.onchange = testVisibility;
        block.childBlocks.link_page.widget.input.onchange = testVisibility;
        testVisibility();

        return block;
    }
}
window.telepath.register('tech_blog_wagtail.base_page.blocks.LinkBlock', LinkBlockDefinition);
